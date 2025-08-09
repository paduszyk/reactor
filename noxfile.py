# /// script
# dependencies = [
#   "dj-database-url>=3.0.1",
#   "nox>=2025.5.1",
#   "python-decouple>=3.8",
# ]
# ///

import json

import dj_database_url as dj_db_url
import nox
from decouple import UndefinedValueError, config

nox.options.default_venv_backend = "uv"
nox.options.envdir = ".nox"
nox.options.reuse_existing_virtualenvs = True

DATABASE_URLS_VARIABLE = "NOX_DATABASE_URLS"


def get_database_urls():
    try:
        database_urls = config(DATABASE_URLS_VARIABLE, cast=json.loads)
    except json.JSONDecodeError as exc_info:
        msg = (
            f"failed to decode the {DATABASE_URLS_VARIABLE} variable; "
            f"expected a dict mapping database aliases to configuration URLs"
        )

        raise ValueError(msg) from exc_info
    except UndefinedValueError:
        database_urls = {"default": None}

    if not isinstance(database_urls, dict):
        msg = (
            f"invalid type for the {DATABASE_URLS_VARIABLE} variable; "
            f"expected a dict, got {type(database_urls).__name__} instead"
        )

        raise TypeError(msg)

    if not database_urls:
        msg = (
            f"the {DATABASE_URLS_VARIABLE} variable is empty; "
            f"expected a dict mapping database aliases to configuration URLs"
        )

        raise ValueError(msg)

    for alias, url in database_urls.items():
        if url is None:
            continue

        try:
            dj_db_url.parse(url)
        except (dj_db_url.ParseError, dj_db_url.UnknownSchemeError) as exc_info:
            msg = (
                f"failed to parse the database configuration URL for alias '{alias}'; "
                f"check the {DATABASE_URLS_VARIABLE} variable"
            )

            raise ValueError(msg) from exc_info

    return database_urls


database_urls = get_database_urls()


@nox.session(python=False, tags=["style", "format"])
def prettier(session):
    session.run("npx", "prettier", "--check", ".", external=True)


@nox.session(python=False, tags=["build"])
def uv(session):
    session.run("uv", "lock", "--check", external=True)


@nox.session(tags=["style"])
@nox.parametrize(
    "args",
    [
        nox.param(["check"], id="check", tags=["lint"]),
        nox.param(["format", "--diff"], id="format", tags=["format"]),
    ],
)
def ruff(session, args):
    session.run_install(
        "uv",
        "sync",
        "--only-group=ruff",
        "--frozen",
        env={
            "UV_PROJECT_ENVIRONMENT": session.virtualenv.location,
        },
    )

    session.run("ruff", *args)


@nox.session(tags=["style"])
@nox.parametrize(
    "args",
    [
        nox.param(["--lint", "--check"], id="lint", tags=["lint"]),
        nox.param(["--reformat", "--check"], id="reformat", tags=["format"]),
    ],
)
def djlint(session, args):
    session.run_install(
        "uv",
        "sync",
        "--only-group=djlint",
        "--frozen",
        env={
            "UV_PROJECT_ENVIRONMENT": session.virtualenv.location,
        },
    )

    session.run("djlint", *args, ".")


@nox.session(tags=["build"])
@nox.parametrize(
    "args",
    [
        nox.param(["check", "--fail-level=ERROR"], id="check"),
        nox.param(["makemigrations", "--check"], id="makemigrations"),
        nox.param(["makemessages", "--all", "--no-location", "--no-obsolete"], id="makemessages"),
    ],
)  # fmt: skip
def django(session, args):
    session.run_install(
        "uv",
        "sync",
        "--no-dev",
        "--frozen",
        env={
            "UV_PROJECT_ENVIRONMENT": session.virtualenv.location,
        },
    )

    session.run("python", "manage.py", *args)

    if args[0] == "makemessages":
        session.run("git", "diff", "--exit-code", ":(glob)**/*.po", external=True)


@nox.session(tags=["test"])
@nox.parametrize(
    "database_url",
    [
        nox.param(
            url,
            id=f"database={alias}",
        )
        for alias, url in database_urls.items()
    ],
)
def pytest(session, database_url):
    session.run_install(
        "uv",
        "sync",
        "--no-dev",
        "--group=pytest",
        "--frozen",
        env={
            "UV_PROJECT_ENVIRONMENT": session.virtualenv.location,
        },
    )

    session.run(
        "pytest",
        "--no-cov",
        *session.posargs,
        env={
            "DJANGO_DATABASE_URL": database_url,
        }
        if database_url
        else {},
    )


if __name__ == "__main__":
    nox.main()

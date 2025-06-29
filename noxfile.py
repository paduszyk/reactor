import json

import nox
from decouple import config

nox.options.default_venv_backend = "uv"
nox.options.envdir = ".nox"
nox.options.reuse_existing_virtualenvs = True


@nox.session(
    python=False,
    tags=[
        "style",
        "format",
    ],
)
def prettier(session):
    session.run(
        *[
            "npx",
            "prettier",
            "--check",
            ".",
        ],
        external=True,
    )


@nox.session(
    python=False,
    tags=[
        "build",
    ],
)
def uv(session):
    session.run(
        *[
            "uv",
            "lock",
            "--check",
        ],
        external=True,
    )


@nox.session(
    requires=[
        "uv",
    ],
    tags=[
        "style",
    ],
)
@nox.parametrize(
    "args",
    [
        nox.param(["check", "."], id="check", tags=["lint"]),
        nox.param(["format", "--diff", "."], id="format", tags=["format"]),
    ],
)
def ruff(session, args):
    session.run_install(
        *[
            "uv",
            "sync",
            "--only-group=ruff",
            "--frozen",
        ],
        env={
            "UV_PROJECT_ENVIRONMENT": session.virtualenv.location,
        },
    )
    session.run("ruff", *args)


@nox.session(
    requires=[
        "uv",
    ],
    tags=[
        "style",
    ],
)
@nox.parametrize(
    "args",
    [
        nox.param(["--lint", "--check", "."], id="lint", tags=["lint"]),
        nox.param(["--reformat", "--check", "."], id="reformat", tags=["format"]),
    ],
)
def djlint(session, args):
    session.run_install(
        *[
            "uv",
            "sync",
            "--only-group=djlint",
            "--frozen",
        ],
        env={
            "UV_PROJECT_ENVIRONMENT": session.virtualenv.location,
        },
    )
    session.run("djlint", *args)


@nox.session(
    requires=[
        "uv",
    ],
    tags=[
        "build",
    ],
)
@nox.parametrize(
    "args",
    [
        nox.param(["check", "--fail-level=ERROR"], id="check"),
        nox.param(["makemigrations", "--check"], id="makemigrations"),
        nox.param(["makemessages", "--all", "--no-location"], id="makemessages"),
    ],
)
def django(session, args):
    session.run_install(
        *[
            "uv",
            "sync",
            "--no-dev",
            "--frozen",
        ],
        env={
            "UV_PROJECT_ENVIRONMENT": session.virtualenv.location,
        },
    )
    session.run("python", "manage.py", *args)

    if "makemessages" in args:
        session.run(
            *[
                "git",
                "diff",
                "--exit-code",
                "*.po",
            ],
            external=True,
        )


def _parse_database_urls(value):
    if value is None:
        return {"default": config("DJANGO_DATABASE_URL")}

    return json.loads(value)


database_urls = config("NOX_DATABASE_URLS", cast=_parse_database_urls, default=None)


@nox.session(
    requires=[
        "uv",
    ],
    tags=[
        "test",
    ],
)
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
        *[
            "uv",
            "sync",
            "--no-dev",
            "--group=pytest",
            "--frozen",
        ],
        env={
            "UV_PROJECT_ENVIRONMENT": session.virtualenv.location,
        },
    )
    session.run(
        *[
            "pytest",
            "--no-cov",
        ],
        env={
            "DATABASE_URL": database_url,
        },
    )

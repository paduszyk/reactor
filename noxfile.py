import json

import nox
from decouple import config as env

nox.options.default_venv_backend = "uv"


@nox.session(python=False)
def uv(session):
    session.run("uv", "lock", "--check", external=True)


@nox.session(requires=["uv"])
@nox.parametrize(
    "args",
    [
        nox.param(["check"], id="check"),
        nox.param(["format", "--diff"], id="format"),
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
    session.run("ruff", *args, ".")


@nox.session(requires=["uv"])
@nox.parametrize(
    "args",
    [
        nox.param(["--lint", "--check"], id="lint"),
        nox.param(["--reformat", "--check"], id="reformat"),
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


@nox.session(requires=["uv"])
@nox.parametrize(
    "args",
    [
        nox.param(
            ["check", "--fail-level=ERROR"],
            id="check",
        ),
        nox.param(
            ["makemigrations", "--check"],
            id="makemigrations",
        ),
        nox.param(
            ["makemessages", "--all", "--no-location", "--no-obsolete"],
            id="makemessages",
        ),
    ],
)
def django(session, args):
    session.run_install(
        "uv",
        "sync",
        "--frozen",
        env={
            "UV_PROJECT_ENVIRONMENT": session.virtualenv.location,
        },
    )
    session.run(
        "python",
        "-m",
        "django",
        *args,
        env={
            "DJANGO_SETTINGS_MODULE": "reactor.conf.settings.dev",
        },
    )

    if args[0] == "makemessages":
        session.run("git", "diff", "--exit-code", ":(glob)**/*.po", external=True)


@nox.session(requires=["uv"])
@nox.parametrize(
    "database_url",
    [
        nox.param(url, id=f"database={alias}")
        for alias, url in (
            env(
                "NOX_DATABASE_URLS",
                cast=json.loads,
                default='{"default": null}',
            )
        ).items()
    ],
)
def pytest(session, database_url):
    session.run_install(
        "uv",
        "sync",
        "--group=pytest",
        "--frozen",
        env={
            "UV_PROJECT_ENVIRONMENT": session.virtualenv.location,
        },
    )
    session.run(
        "pytest",
        env={
            "DJANGO_DATABASE_URL": database_url,
        }
        if database_url
        else {},
    )

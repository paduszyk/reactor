import json

import nox
from decouple import config

nox.options.default_venv_backend = "uv"
nox.options.envdir = ".nox"
nox.options.reuse_existing_virtualenvs = True


@nox.session(python=False, tags=["format", "style"])
def prettier(session):
    session.run("npx", "prettier", "--check", ".", external=True)


@nox.session(python=False)
def uv_lock(session):
    session.run("uv", "lock", "--check", external=True)


@nox.session(requires=["uv_lock"], tags=["style"])
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
    session.run("ruff", *args, ".")


@nox.session(requires=["uv_lock"], tags=["style"])
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


@nox.session(requires=["uv_lock"])
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
        "uv",
        "sync",
        "--no-dev",
        "--frozen",
        env={
            "UV_PROJECT_ENVIRONMENT": session.virtualenv.location,
        },
    )
    session.run("python", "manage.py", *args)


@nox.session(requires=["uv_lock"], tags=["test"])
@nox.parametrize(
    "database_url",
    [
        nox.param(url, id=alias, tags=[alias])
        for alias, url in config(
            "NOX_DATABASE_URLS",
            cast=json.loads,
            default=f'{{ "default": "{config("DJANGO_DATABASE_URL")}" }}',
        ).items()
    ],
)
def pytest(session, database_url):
    session.run_install(
        "uv",
        "sync",
        "--no-dev",
        "--group=tests",
        "--frozen",
        env={
            "UV_PROJECT_ENVIRONMENT": session.virtualenv.location,
        },
    )
    session.run("pytest", "--no-cov", env={"DJANGO_DATABASE_URL": database_url})

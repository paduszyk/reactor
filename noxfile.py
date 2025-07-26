import nox

nox.options.default_venv_backend = "uv"
nox.options.envdir = ".nox"
nox.options.reuse_existing_virtualenvs = True


@nox.session(python=False, tags=["format", "style"])
def prettier(session):
    session.run("npx", "prettier", "--check", ".", external=True)


@nox.session(python=False, tags=["build"])
def uv(session):
    session.run("uv", "lock", "--check", external=True)


@nox.session(requires=["uv"], tags=["style"])
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


@nox.session(requires=["uv"], tags=["style"])
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


@nox.session(requires=["uv"], tags=["build"])
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
        "--frozen",
        env={
            "UV_PROJECT_ENVIRONMENT": session.virtualenv.location,
        },
    )

    session.run("python", "manage.py", *args)

    if args[0] == "makemessages":
        session.run("git", "diff", "--exit-code", "*.po", external=True)


@nox.session(requires=["uv"], tags=["test"])
def pytest(session):
    session.run_install(
        "uv",
        "sync",
        "--group=pytest",
        "--frozen",
        env={
            "UV_PROJECT_ENVIRONMENT": session.virtualenv.location,
        },
    )

    session.run("pytest", "--no-cov")

import nox


@nox.session(
    name="uv.lock check",
    python=False,
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
    name="Ruff ",
    venv_backend="uv",
    reuse_venv=True,
)
@nox.parametrize(
    "args",
    [
        nox.param(args, id=alias)
        for alias, args in {
            "linter": ["check"],
            "formatter": ["format", "--check"],
        }.items()
    ],
)
def ruff(session, args):
    session.run_install(
        *[
            "uv",
            "sync",
            "--only-group",
            "ruff",
            "--frozen",
        ],
        env={
            "UV_PROJECT_ENVIRONMENT": session.virtualenv.location,
        },
    )

    session.run("ruff", *args)


@nox.session(
    name="djLint ",
    venv_backend="uv",
    reuse_venv=True,
)
@nox.parametrize(
    "args",
    [
        nox.param(args, id=alias)
        for alias, args in {
            "linter": ["--lint", "--check"],
            "formatter": ["--reformat", "--check"],
        }.items()
    ],
)
def djlint(session, args):
    session.run_install(
        *[
            "uv",
            "sync",
            "--only-group",
            "djlint",
            "--frozen",
        ],
        env={
            "UV_PROJECT_ENVIRONMENT": session.virtualenv.location,
        },
    )

    session.run("djlint", *args, ".")


@nox.session(
    name="Django ",
    venv_backend="uv",
    reuse_venv=True,
)
@nox.parametrize(
    "args",
    [
        nox.param(args, id=alias)
        for alias, args in {
            "system check": ["check"],
            "migrations check": ["makemigrations", "--check"],
        }.items()
    ],
)
def django(session, args):
    session.run_install(
        *[
            "uv",
            "sync",
            "--frozen",
        ],
        env={
            "UV_PROJECT_ENVIRONMENT": session.virtualenv.location,
        },
    )

    session.run("python", "manage.py", *args)


@nox.session(
    name="Pytest",
    venv_backend="uv",
    reuse_venv=True,
)
def pytest(session):
    session.run_install(
        *[
            "uv",
            "sync",
            "--group",
            "tests",
            "--frozen",
        ],
        env={
            "UV_PROJECT_ENVIRONMENT": session.virtualenv.location,
        },
    )

    session.run("pytest", *session.posargs)

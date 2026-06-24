import nox
import nox_uv
from environs import env

env.read_env()

nox.needs_version = ">=2026.4.10"

nox.options.envdir = ".nox"
nox.options.default_venv_backend = "uv"

_MISSING = object()

_DATABASE_URLS = env.dict("NOX_DATABASE_URLS", default=_MISSING)


@nox.session(python=False)
@nox.parametrize(
    "args",
    [
        nox.param(["sync", "--check"], id="sync"),
        nox.param(["lock", "--check"], id="lock"),
    ],
)
def uv(session, args):
    session.run("uv", *args, external=True)


@nox_uv.session(uv_only_groups=["ruff"])
@nox.parametrize(
    "args",
    [
        nox.param(["check"], id="check"),
        nox.param(["format", "--diff"], id="format"),
    ],
)
def ruff(session, args):
    session.run("ruff", *args, ".")


@nox_uv.session(uv_only_groups=["djlint"])
@nox.parametrize(
    "args",
    [
        nox.param(["--lint", "--check"], id="lint"),
        nox.param(["--reformat", "--check"], id="reformat"),
    ],
)
def djlint(session, args):
    session.run("djlint", *args, ".")


@nox_uv.session
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


if _DATABASE_URLS is _MISSING:

    @nox_uv.session(uv_groups=["pytest"])
    def pytest(session):
        session.run("pytest")

else:

    @nox_uv.session(uv_groups=["pytest"])
    @nox.parametrize(
        "database_url",
        [
            nox.param(
                database_url,
                id=f"database='{alias}'",
            )
            for alias, database_url in _DATABASE_URLS.items()
        ],
    )
    def pytest(session, database_url):
        session.run(
            "pytest",
            env={
                "DJANGO_DATABASE_URL": database_url,
            },
        )

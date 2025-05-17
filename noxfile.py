import nox
import pytest
from environs import env

DATABASE_URLS = env.dict("NOX_DATABASE_URLS")

PYTEST_ARGS = env.list("NOX_PYTEST_ARGS", delimiter=" ", default=[])

SESSION_RUN_SILENT = env.bool("NOX_SESSION_RUN_SILENT", default=False)


@nox.session(
    python=False,
    name="Tests ",
)
@nox.parametrize(
    "database_url",
    [
        nox.param(
            url,
            id=alias,
        )
        for alias, url in DATABASE_URLS.items()
    ],
)
def tests(session, database_url):
    session.run(
        "pytest",
        *PYTEST_ARGS,
        env={
            "DJANGO_DATABASE_URL": database_url,
        },
        silent=SESSION_RUN_SILENT,
        success_codes=[
            pytest.ExitCode.OK,
            pytest.ExitCode.NO_TESTS_COLLECTED,
        ],
        external=True,
    )

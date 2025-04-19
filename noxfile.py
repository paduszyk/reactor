from functools import partial

import nox
from decouple import Csv, config

DATABASE_URLS = config(
    "NOX_DATABASE_URLS",
    cast=Csv(
        cast=partial(str.split, sep="="),
        post_process=dict,
    ),
)

PYTEST_ARGS = config("NOX_PYTEST_ARGS", cast=Csv(delimiter=" "), default="")

SILENT = config("NOX_SILENT", cast=bool, default=False)


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
        silent=SILENT,
        external=True,
    )

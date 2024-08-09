__all__ = [
    "CoreConf",
]

import appconf


class CoreConf(appconf.AppConf):
    """Encapsulates settings specific to the `core` app."""

    class Meta:
        prefix = "reactor"


settings = CoreConf()

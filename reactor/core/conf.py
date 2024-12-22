import appconf


class CoreConf(appconf.AppConf):
    class Meta:
        prefix = "reactor"


settings = CoreConf()

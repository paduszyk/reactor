from reactor.conf.settings import dev


class Settings(dev.Settings):
    # Apps

    @property
    def INSTALLED_APPS(self):
        return [
            *super().INSTALLED_APPS,
            "tests",
        ]

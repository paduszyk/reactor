from . import debug


class Settings(debug.Settings):
    # Databases

    @property
    def DATABASES(self):
        return {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": self.BASE_DIR / "db.sqlite3",
            },
        }

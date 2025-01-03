from . import debug


class Settings(debug.Settings):
    @classmethod
    def pre_load(cls):
        from dotenv import load_dotenv

        load_dotenv()

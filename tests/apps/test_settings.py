from reactor.apps.settings import AppSettings as BaseFirstPartyAppSettings


def test_app_settings_subclass_updates_django_settings(django_settings):
    # Arrange.
    def load_app_settings():
        class AppSettings(BaseFirstPartyAppSettings):
            SETTING_NAME = "app_setting_value"

            class Meta:
                prefix = "app"

        return AppSettings()

    # Act.
    app_settings = load_app_settings()

    # Assert.
    assert app_settings.SETTING_NAME == "app_setting_value"
    assert django_settings.APP_SETTING_NAME == "app_setting_value"


def test_app_settings_subclass_prefers_django_setting(django_settings):
    # Arrange.
    django_settings.APP_SETTING_NAME = "django_setting_value"

    def load_app_settings():
        class AppSettings(BaseFirstPartyAppSettings):
            SETTING_NAME = "app_settings_value"

            class Meta:
                prefix = "app"

        return AppSettings()

    # Act.
    app_settings = load_app_settings()

    # Assert.
    assert app_settings.SETTING_NAME == "django_setting_value"
    assert django_settings.APP_SETTING_NAME == "django_setting_value"


def test_app_settings_subclass_configures_setting_value(django_settings):
    # Arrange.
    def load_app_settings():
        class AppSettings(BaseFirstPartyAppSettings):
            SETTING_NAME = "app_setting_value"

            class Meta:
                prefix = "app"

            def configure_setting_name(self, value):
                return f"configured_{value}"

        return AppSettings()

    # Act.
    app_settings = load_app_settings()

    # Assert.
    assert app_settings.SETTING_NAME == "configured_app_setting_value"
    assert django_settings.APP_SETTING_NAME == "configured_app_setting_value"

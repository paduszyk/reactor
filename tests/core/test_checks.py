from reactor.core.checks import check_app_config_base_class, check_model_base_class


def test_app_config_base_class_returns_e001_if_invalid_app_config_base_class(mocker):
    # Arrange.
    class MockAppConfig:
        label = "mock_app"

    mock_app_config = MockAppConfig()

    # Mock.
    mocker.patch(
        "reactor.core.checks.apps.get_app_configs",
        return_value=[mock_app_config],
    )

    # Act.
    messages = check_app_config_base_class()

    # Assert.
    assert len(messages) == 1
    assert messages[0].id == "reactor.E001"


def test_model_base_class_returns_e002_if_invalid_model_base_class(mocker):
    # Arrange.
    class MockModel:
        class Meta:
            label = "mock_model"

        _meta = Meta()

    # Mock.
    mocker.patch(
        "reactor.core.checks.apps.get_models",
        return_value=[MockModel],
    )

    # Act.
    messages = check_model_base_class()

    # Assert.
    assert len(messages) == 1
    assert messages[0].id == "reactor.E002"

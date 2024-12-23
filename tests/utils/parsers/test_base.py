from reactor.utils.parsers.base import Parser


def test_parser_getattr_returns_raw_value_if_setup_fails_and_attr_is_public():
    # Arrange.
    class ParserSetupError(Exception):
        pass

    class MockParser(Parser):
        public_attr = "public_attr"

        def _setup(self, raw_value):
            if raw_value == "invalid_value":
                raise ParserSetupError

    mock_parser = MockParser("invalid_value")

    # Act & assert.
    assert mock_parser.public_attr == "invalid_value"


def test_parser_getattr_returns_attr_value_if_setup_fails_and_attr_is_private():
    # Arrange.
    class ParserSetupError(Exception):
        pass

    class MockParser(Parser):
        _private_attr = "private_attr"

        def _setup(self, raw_value):
            if raw_value == "invalid_value":
                raise ParserSetupError

    mock_parser = MockParser("invalid_value")

    # Act & assert.
    assert mock_parser._private_attr == "private_attr"  # noqa: SLF001

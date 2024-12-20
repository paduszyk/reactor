from reactor.utils.parsers.base import Parser


def test_parser_getattr_returns_raw_value_if_setup_fails():
    # Arrange.
    class ParserSetupError(Exception):
        pass

    class MockParser(Parser):
        public_attr = "public_attr"

        def setup(self, raw_value):
            if raw_value == "invalid_value":
                raise ParserSetupError

    mock_parser = MockParser("invalid_value")

    # Act & assert.
    assert mock_parser.public_attr == "invalid_value"


def test_parser_setup_failed_returns_true_if_setup_fails():
    # Arrange.
    class ParserSetupError(Exception):
        pass

    class MockParser(Parser):
        def setup(self, raw_value):
            if raw_value == "invalid_value":
                raise ParserSetupError

    mock_parser = MockParser("invalid_value")

    # Act & assert.
    assert mock_parser.setup_failed is True

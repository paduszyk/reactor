import pytest

from reactor.utils.parsers.human_name import HumanName


@pytest.mark.parametrize(
    ("raw_value", "parsed_value"),
    [
        ("Doe, Joe", "Doe"),
        ("Doe, Joe Mark Anthony", "Doe"),
        ("Doe-Smith, Joe Mark Anthony", "Doe-Smith"),
        ("Doe, Joe-Mark Anthony", "Doe"),
        ("Doe, Joe Mark-Anthony", "Doe"),
        ("Doe, Joe  Mark  Anthony", "Doe"),
    ],
)
def test_human_name_last(raw_value, parsed_value):
    # Arrange.
    human_name = HumanName(raw_value)

    # Act & assert.
    assert human_name.last == parsed_value


@pytest.mark.parametrize(
    ("raw_value", "parsed_value"),
    [
        ("Doe, Joe", "Joe"),
        ("Doe, Joe Mark Anthony", "Joe Mark Anthony"),
        ("Doe-Smith, Joe Mark Anthony", "Joe Mark Anthony"),
        ("Doe, Joe-Mark Anthony", "Joe-Mark Anthony"),
        ("Doe, Joe Mark-Anthony", "Joe Mark-Anthony"),
        ("Doe, Joe  Mark  Anthony", "Joe Mark Anthony"),
    ],
)
def test_human_name_given(raw_value, parsed_value):
    # Arrange.
    human_name = HumanName(raw_value)

    # Act & assert.
    assert human_name.given == parsed_value


@pytest.mark.parametrize(
    ("raw_value", "parsed_value"),
    [
        ("Doe, Joe", "Joe"),
        ("Doe, Joe Mark Anthony", "Joe"),
        ("Doe-Smith, Joe Mark Anthony", "Joe"),
        ("Doe, Joe-Mark Anthony", "Joe-Mark"),
        ("Doe, Joe Mark-Anthony", "Joe"),
        ("Doe, Joe  Mark  Anthony", "Joe"),
    ],
)
def test_human_name_first(raw_value, parsed_value):
    # Arrange.
    human_name = HumanName(raw_value)

    # Act & assert.
    assert human_name.first == parsed_value


@pytest.mark.parametrize(
    ("raw_value", "parsed_value"),
    [
        ("Doe, Joe", ""),
        ("Doe, Joe Mark Anthony", "Mark Anthony"),
        ("Doe-Smith, Joe Mark Anthony", "Mark Anthony"),
        ("Doe, Joe-Mark Anthony", "Anthony"),
        ("Doe, Joe Mark-Anthony", "Mark-Anthony"),
        ("Doe, Joe  Mark  Anthony", "Mark Anthony"),
    ],
)
def test_human_name_middle(raw_value, parsed_value):
    # Arrange.
    human_name = HumanName(raw_value)

    # Act & assert.
    assert human_name.middle == parsed_value


@pytest.mark.parametrize(
    ("raw_value", "parsed_value"),
    [
        ("Doe, Joe", "Joe Doe"),
        ("Doe, Joe Mark Anthony", "Joe M. A. Doe"),
        ("Doe-Smith, Joe Mark Anthony", "Joe M. A. Doe-Smith"),
        ("Doe, Joe-Mark Anthony", "Joe-Mark A. Doe"),
        ("Doe, Joe Mark-Anthony", "Joe M.-A. Doe"),
        ("Doe, Joe  Mark  Anthony", "Joe M. A. Doe"),
    ],
)
def test_human_name_full(raw_value, parsed_value):
    # Arrange.
    human_name = HumanName(raw_value)

    # Act & assert.
    assert human_name.full == parsed_value


@pytest.mark.parametrize(
    ("raw_value", "parsed_value"),
    [
        ("Doe, Joe", "Doe Joe"),
        ("Doe, Joe Mark Anthony", "Doe Joe M. A."),
        ("Doe-Smith, Joe Mark Anthony", "Doe-Smith Joe M. A."),
        ("Doe, Joe-Mark Anthony", "Doe Joe-Mark A."),
        ("Doe, Joe Mark-Anthony", "Doe Joe M.-A."),
        ("Doe, Joe  Mark  Anthony", "Doe Joe M. A."),
    ],
)
def test_human_name_full_reversed(raw_value, parsed_value):
    # Arrange.
    human_name = HumanName(raw_value)

    # Act & assert.
    assert human_name.full_reversed == parsed_value


@pytest.mark.parametrize(
    ("raw_value", "parsed_value"),
    [
        ("Doe, Joe", "J. Doe"),
        ("Doe, Joe Mark Anthony", "J. M. A. Doe"),
        ("Doe-Smith, Joe Mark Anthony", "J. M. A. Doe-Smith"),
        ("Doe, Joe-Mark Anthony", "J.-M. A. Doe"),
        ("Doe, Joe Mark-Anthony", "J. M.-A. Doe"),
        ("Doe, Joe  Mark  Anthony", "J. M. A. Doe"),
    ],
)
def test_human_name_short(raw_value, parsed_value):
    # Arrange.
    human_name = HumanName(raw_value)

    # Act & assert.
    assert human_name.short == parsed_value


@pytest.mark.parametrize(
    ("raw_value", "parsed_value"),
    [
        ("Doe, Joe", "Doe J."),
        ("Doe, Joe Mark Anthony", "Doe J. M. A."),
        ("Doe-Smith, Joe Mark Anthony", "Doe-Smith J. M. A."),
        ("Doe, Joe-Mark Anthony", "Doe J.-M. A."),
        ("Doe, Joe Mark-Anthony", "Doe J. M.-A."),
        ("Doe, Joe  Mark  Anthony", "Doe J. M. A."),
    ],
)
def test_human_name_short_reversed(raw_value, parsed_value):
    # Arrange.
    human_name = HumanName(raw_value)

    # Act & assert.
    assert human_name.short_reversed == parsed_value


@pytest.mark.parametrize(
    ("raw_value", "parsed_value"),
    [
        ("Doe, Joe", "J. D."),
        ("Doe, Joe Mark Anthony", "J. M. A. D."),
        ("Doe-Smith, Joe Mark Anthony", "J. M. A. D.-S."),
        ("Doe, Joe-Mark Anthony", "J.-M. A. D."),
        ("Doe, Joe Mark-Anthony", "J. M.-A. D."),
        ("Doe, Joe  Mark  Anthony", "J. M. A. D."),
    ],
)
def test_human_name_initials(raw_value, parsed_value):
    # Arrange.
    human_name = HumanName(raw_value)

    # Act & assert.
    assert human_name.initials == parsed_value

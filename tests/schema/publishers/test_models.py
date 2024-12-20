import pytest


@pytest.mark.django_db
def test_publishing_house_str(baker):
    # Arrange.
    publishing_house = baker.make(
        "publishers.PublishingHouse",
        name="American Chemical Society",
        abbreviation="ACS",
    )

    # Act.
    publishing_house_str = str(publishing_house)

    # Assert.
    assert publishing_house_str == "American Chemical Society (ACS)"


@pytest.mark.django_db
def test_journal_str(baker):
    # Arrange.
    publishing_house = baker.make(
        "publishers.PublishingHouse",
        abbreviation="ACS",
    )
    journal = baker.make(
        "publishers.Journal",
        title="Journal of Medicinal Chemistry",
        publishing_house=publishing_house,
    )

    # Act.
    journal_str = str(journal)

    # Assert.
    assert journal_str == "Journal of Medicinal Chemistry (ACS)"

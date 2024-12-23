import pytest

from django.utils import translation


@pytest.mark.django_db
def test_degree_str(baker):
    # Arrange.
    degree = baker.make(
        "evaluation.Degree",
        name="prof.",
    )

    # Act.
    degree_str = str(degree)

    # Assert.
    assert degree_str == "prof."


@pytest.mark.django_db
def test_domain_str(baker):
    # Arrange.
    domain = baker.make(
        "evaluation.Domain",
        name="natural sciences",
    )

    # Act.
    domain_str = str(domain)

    # Assert.
    assert domain_str == "natural sciences"


@pytest.mark.django_db
def test_discipline_str(baker):
    # Arrange.
    domain = baker.make(
        "evaluation.Domain",
        name="natural sciences",
    )
    discipline = baker.make(
        "evaluation.Discipline",
        name="chemistry",
        domain=domain,
    )

    # Act.
    with translation.override("en"):
        discipline_str = str(discipline)

    # Assert.
    assert discipline_str == "chemistry (in domain: natural sciences)"

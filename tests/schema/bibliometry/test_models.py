from datetime import date
from decimal import Decimal

import pytest

from django.utils import translation


@pytest.mark.django_db
def test_impact_factor_str(baker):
    # Arrange.
    publishing_house = baker.make(
        "publishers.PublishingHouse",
        abbreviation="ACS",
    )
    journal = baker.make(
        "publishers.Journal",
        abbreviation="J. Med. Chem.",
        publishing_house=publishing_house,
    )
    impact_factor = baker.make(
        "bibliometry.ImpactFactor",
        year_published=2020,
        value_2_year=Decimal("3.456"),
        value_5_year=Decimal("4.567"),
        journal=journal,
    )

    # Act.
    with translation.override("en"):
        impact_factor_str = str(impact_factor)

    # Assert.
    assert impact_factor_str == (
        "IF[J. Med. Chem. (ACS); 2020] = 3.456 (2-year) / 4.567 (5-year)"
    )


@pytest.mark.django_db
def test_ministry_score_str(baker):
    # Arrange.
    publishing_house = baker.make(
        "publishers.PublishingHouse",
        abbreviation="ACS",
    )
    journal = baker.make(
        "publishers.Journal",
        abbreviation="J. Med. Chem.",
        publishing_house=publishing_house,
    )
    ministry_score = baker.make(
        "bibliometry.MinistryScore",
        value=140,
        date_published=date(2020, 1, 1),
        journal=journal,
    )

    # Act.
    with translation.override("en"):
        ministry_score_str = str(ministry_score)

    # Assert.
    assert ministry_score_str == "MS[J. Med. Chem. (ACS); 2020-01-01] = 140"

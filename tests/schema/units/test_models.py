import pytest


@pytest.mark.django_db
def test_institution_str(baker):
    # Arrange.
    institution = baker.make(
        "units.Institution",
        name="Warsaw University of Technology",
        abbreviation="WUT",
    )

    # Act.
    institution_str = str(institution)

    # Assert.
    assert institution_str == "Warsaw University of Technology (WUT)"


@pytest.mark.django_db
def test_institute_str(baker):
    # Arrange.
    institution = baker.make(
        "units.Institution",
        name="Warsaw University of Technology",
        abbreviation="WUT",
    )
    institute = baker.make(
        "units.Institute",
        name="Faculty of Chemistry",
        abbreviation="Chem",
        institution=institution,
    )

    # Act.
    institute_str = str(institute)

    # Assert.
    assert institute_str == (
        "Faculty of Chemistry, Warsaw University of Technology (Chem/WUT)"
    )


@pytest.mark.django_db
def test_department_str(baker):
    # Arrange.
    institution = baker.make(
        "units.Institution",
        name="Warsaw University of Technology",
        abbreviation="WUT",
    )
    institute = baker.make(
        "units.Institute",
        name="Faculty of Chemistry",
        abbreviation="Chem",
        institution=institution,
    )
    department = baker.make(
        "units.Department",
        name="Department of Physical Chemistry",
        abbreviation="Phys",
        institute=institute,
    )

    # Act.
    department_str = str(department)

    # Assert.
    assert department_str == (
        "Department of Physical Chemistry, "
        "Faculty of Chemistry, Warsaw University of Technology (Phys/Chem/WUT)"
    )

import pytest

from django.utils import translation


@pytest.mark.django_db
def test_person_str(baker):
    # Arrange.
    degree = baker.make(
        "evaluation.Degree",
        name="prof.",
    )
    person = baker.make(
        "hr.Person",
        last_name="Doe",
        given_names="Joe Mark Anthony",
        degree=degree,
    )

    # Act.
    person_str = str(person)

    # Assert.
    assert person_str == "Joe M. A. Doe, prof."


@pytest.mark.django_db
def test_status_str(baker):
    # Arrange.
    status = baker.make(
        "hr.Status",
        name="employee",
    )

    # Act.
    status_str = str(status)

    # Assert.
    assert status_str == "employee"


@pytest.mark.django_db
def test_group_str(baker):
    # Arrange.
    group = baker.make(
        "hr.Group",
        name="academic teachers",
    )

    # Act.
    group_str = str(group)

    # Assert.
    assert group_str == "academic teachers"


@pytest.mark.django_db
def test_subgroup_str(baker):
    # Arrange.
    group = baker.make(
        "hr.Group",
        name="academic teachers",
    )
    subgroup = baker.make(
        "hr.Subgroup",
        name="researchers",
        group=group,
    )

    # Act.
    with translation.override("en"):
        subgroup_str = str(subgroup)

    # Assert.
    assert subgroup_str == "researchers (in group: academic teachers)"


@pytest.mark.django_db
def test_position_str(baker):
    # Arrange.
    subgroup = baker.make(
        "hr.Subgroup",
        name="researchers",
    )
    position = baker.make(
        "hr.Position",
        name="assistant professor",
        subgroup=subgroup,
    )

    # Act.
    with translation.override("en"):
        position_str = str(position)

    # Assert.
    assert position_str == "assistant professor (in subgroup: researchers)"


@pytest.mark.django_db
def test_contract_str(baker):
    # Arrange.
    person = baker.make(
        "hr.Person",
        last_name="Doe",
        given_names="Joe Mark Anthony",
    )
    status = baker.make(
        "hr.Status",
        name="employee",
    )
    institution = baker.make(
        "units.Institution",
        abbreviation="WUT",
    )
    institute = baker.make(
        "units.Institute",
        abbreviation="Chem",
        institution=institution,
    )
    department = baker.make(
        "units.Department",
        abbreviation="Phys",
        institute=institute,
    )
    contract = baker.make(
        "hr.Contract",
        person=person,
        status=status,
        unit=department,
    )

    # Act.
    contract_str = str(contract)

    # Assert.
    assert contract_str == "Doe Joe M. A. (employee at Phys/Chem/WUT)"

__all__ = [
    "ContractAdmin",
    "GroupAdmin",
    "PersonAdmin",
    "PositionAdmin",
    "StatusAdmin",
    "SubgroupAdmin",
]

from reactor import admin
from reactor.schema.human_resources.models import (
    Contract,
    Group,
    Person,
    Position,
    Status,
    Subgroup,
)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Subgroup)
class SubgroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    pass

__all__ = [
    "DegreeAdmin",
    "DisciplineAdmin",
    "DomainAdmin",
]

from reactor import admin
from reactor.schema.science_classification.models import Degree, Discipline, Domain


@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    pass


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    pass


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    pass

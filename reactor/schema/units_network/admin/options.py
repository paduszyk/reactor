__all__ = [
    "DepartmentAdmin",
    "FacultyAdmin",
    "UniversityAdmin",
]

from reactor import admin
from reactor.schema.units_network.models import Department, Faculty, University


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    pass


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    pass


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass

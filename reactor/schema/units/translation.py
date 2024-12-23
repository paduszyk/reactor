from modeltranslation import translator

from .models import Department, Institute, Institution


@translator.register(Institution)
class InstitutionTranslationOptions(translator.TranslationOptions):
    fields = [
        "name",
        "abbreviation",
    ]


@translator.register(Institute)
class InstituteTranslationOptions(translator.TranslationOptions):
    fields = [
        "name",
        "abbreviation",
    ]


@translator.register(Department)
class DepartmentTranslationOptions(translator.TranslationOptions):
    fields = [
        "name",
        "abbreviation",
    ]

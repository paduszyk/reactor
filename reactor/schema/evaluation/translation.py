from modeltranslation import translator

from .models import Degree, Discipline, Domain


@translator.register(Degree)
class DegreeTranslationOptions(translator.TranslationOptions):
    fields = [
        "name",
    ]


@translator.register(Domain)
class DomainTranslationOptions(translator.TranslationOptions):
    fields = [
        "name",
    ]


@translator.register(Discipline)
class DisciplineTranslationOptions(translator.TranslationOptions):
    fields = [
        "name",
    ]

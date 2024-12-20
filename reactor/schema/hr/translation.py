from modeltranslation import translator

from .models import Group, Position, Status, Subgroup


@translator.register(Status)
class StatusTranslationOptions(translator.TranslationOptions):
    fields = [
        "name",
    ]


@translator.register(Group)
class GroupTranslationOptions(translator.TranslationOptions):
    fields = [
        "name",
    ]


@translator.register(Subgroup)
class SubgroupTranslationOptions(translator.TranslationOptions):
    fields = [
        "name",
    ]


@translator.register(Position)
class PositionTranslationOptions(translator.TranslationOptions):
    fields = [
        "name",
    ]

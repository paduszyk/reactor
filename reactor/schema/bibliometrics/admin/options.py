__all__ = [
    "ImpactFactorAdmin",
    "MinisterialRatingAdmin",
]

from reactor import admin
from reactor.schema.bibliometrics.models import ImpactFactor, MinisterialRating


@admin.register(ImpactFactor)
class ImpactFactorAdmin(admin.ModelAdmin):
    pass


@admin.register(MinisterialRating)
class MinisterialRatingAdmin(admin.ModelAdmin):
    pass

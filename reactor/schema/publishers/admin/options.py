__all__ = [
    "JournalAdmin",
    "PublishingHouseAdmin",
]

from reactor import admin
from reactor.schema.publishers.models import Journal, PublishingHouse


@admin.register(PublishingHouse)
class PublishingHouseAdmin(admin.ModelAdmin):
    pass


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    pass

__all__ = [
    "ArticleAdmin",
    "ArticleContributionAdmin",
    "AuthorAdmin",
]

from reactor import admin
from reactor.schema.research_output.models import Article, ArticleContribution, Author


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(ArticleContribution)
class ArticleContributionAdmin(admin.ModelAdmin):
    pass

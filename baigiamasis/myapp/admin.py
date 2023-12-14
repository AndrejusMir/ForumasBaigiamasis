from django.contrib import admin
from .models import Article
from .models import AdminPanel

admin.site.register(AdminPanel)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'approved', 'published_date']
    actions = ['approve_articles']

    def approve_articles(self, request, queryset):
        queryset.update(approved=True)
    approve_articles.short_description = "Approve selected articles"



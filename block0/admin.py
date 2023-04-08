from django.contrib import admin
from . import models


class CommentInline(admin.StackedInline):
    model = models.Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_date')
    list_filter = ['publication_date']
    search_fields = ['title']

    fieldsets = [
        ('Post content', {'fields': ['title', 'content', 'author']}),
        ('Date information', {'fields': ['publication_date']}),
    ]

    inlines = [CommentInline]


# Register your models here.
admin.site.register(models.Post, PostAdmin)

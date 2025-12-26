from django.contrib import admin
from .models import Novel, Chapter


@admin.register(Novel)
class NovelAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at', 'updated_at')
    search_fields = ('title', 'summary', 'author__username')
    list_filter = ('status', 'created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'novel', 'order', 'created_at')
    search_fields = ('title', 'novel__title')
    list_filter = ('created_at',)
    ordering = ('novel', 'order')

# Register your models here.

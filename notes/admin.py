from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'author')
    search_fields = ('title', 'content', 'author__username')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

# Register your models here.

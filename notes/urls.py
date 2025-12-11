from django.urls import path
from . import views

app_name = "notes"

urlpatterns = [
    path("", views.note_list, name="note_list"),
    path("delete/", views.note_delete, name="note_delete"),
    path("write/", views.note_form, name="note_form"),
    path("write/<int:pk>/", views.note_form, name="note_detail"),
]
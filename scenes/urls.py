from django.urls import path
from . import views

app_name = 'scenes' 

urlpatterns = [
    path('', views.scene_list, name='scene_list'),
    path('create/', views.scene_create, name='scene_create'),
    path('<int:pk>/edit/', views.scene_edit, name='scene_edit'),
]
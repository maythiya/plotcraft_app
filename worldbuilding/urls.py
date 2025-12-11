from django.urls import path
from . import views


urlpatterns = [
    path('', views.overview, name='overview'),

    #Characters
    path('characters/', views.character_list, name='character_list'),
    path('characters/create/', views.character_create, name='character_create'),
    path('characters/<int:pk>/', views.character_detail, name='character_detail'),
    path('characters/<int:pk>/edit/', views.character_edit, name='character_edit'),

    #Locations
    path('locations/', views.location_list, name='location_list'),           
    path('locations/create/', views.location_create, name='location_create'), 
    path('locations/<int:pk>/', views.location_detail, name='location_detail'),
    path('locations/<int:pk>/edit/', views.location_edit, name='location_edit'),

    #Items
    path('items/', views.item_list, name='item_list'),
    path('items/create/', views.item_create, name='item_create'),
    path('items/<int:pk>/', views.item_detail, name='item_detail'),
    path('items/<int:pk>/edit/', views.item_edit, name='item_edit'),
]
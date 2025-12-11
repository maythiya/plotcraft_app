from django.urls import path
from . import views

app_name = 'timeline'

urlpatterns = [
# หน้ารายการ (List)
    path('', views.timeline_list, name='timeline_list'),
    path('create/', views.timeline_create, name='timeline_create'),
    path('<int:pk>/', views.timeline_detail, name='timeline_detail'),


    path('<int:pk>/event/create/', views.timeline_event_create, name='timeline_event_create'),
    path('<int:pk>/delete/', views.timeline_delete, name='timeline_delete'),
    path('event/<int:pk>/update/', views.timeline_event_update, name='timeline_event_update'),
    path('event/<int:pk>/delete/', views.timeline_event_delete, name='timeline_event_delete'),
    path('reorder/', views.update_event_order, name='update_event_order'),


]

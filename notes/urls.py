from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    # ชั้นหนังสือ
    path('', views.novel_list, name='novel_list'),
    
    # สร้างนิยายใหม่
    path('create/', views.novel_create, name='novel_create'),
    
    # หน้าจัดการนิยาย (Dashboard)
    path('<int:pk>/', views.novel_detail, name='novel_detail'),
    path('delete/<int:pk>/', views.novel_delete, name='novel_delete'),
    path('<int:pk>/edit/', views.novel_edit, name='novel_edit'),
    
    # สร้างตอนใหม่ (กรอกข้อมูลเบื้องต้น)
    path('<int:novel_id>/chapter/add/', views.chapter_create, name='chapter_create'),
    
    # หน้าเขียนเนื้อหา (Editor)
    path('<int:novel_id>/chapter/<int:chapter_id>/write/', views.chapter_edit, name='chapter_edit'),
    
    # ลบตอน
    path('chapter/<int:pk>/delete/', views.chapter_delete, name='chapter_delete'),
]
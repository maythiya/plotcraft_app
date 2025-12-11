from django.contrib import admin
from .models import Scene

@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    # แสดงคอลัมน์: ชื่อฉาก, คนสร้าง, วันที่สร้าง, สถานะ
    list_display = ('title', 'created_by', 'created_at', 'status')
    
    # เพิ่มตัวกรองด้านขวา: กรองตามสถานะ และ วันที่สร้าง
    list_filter = ('status', 'created_at')
    
    # เพิ่มช่องค้นหาด้านบน: ค้นหาจากชื่อฉาก
    search_fields = ('title',)
    
# Register your models here.

from django.contrib import admin
from .models import Character, Location

# กำหนดค่า AdminSite เบื้องต้น (ถ้าต้องการปรับ header/title ของหน้า admin)
class WorldbuildingAdmin(admin.AdminSite):
    site_header = "Worldbuilding Administration"
    site_title = "Worldbuilding Admin Portal"
    index_title = "Welcome to the Worldbuilding Admin Area"


# กำหนด ModelAdmin สำหรับ `Character` เพื่อระบุคอลัมน์ที่จะแสดงใน list view
@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    # รายการคอลัมน์ที่จะแสดงในหน้า change list ของ admin
    # - 'project': มาจากเรื่อง/โปรเจ็กต์ไหน
    # - 'name': ชื่อตัวละคร
    # - 'created_at': วันที่สร้างเรคคอร์ด
    # - 'created_by': ผู้ใช้ที่เป็นผู้สร้าง
    list_display = ('project', 'name', 'created_at', 'created_by')

    # ฟิลด์ที่ใช้เป็นตัวกรองทางขวามือของหน้า admin (ช่วยกรองเรคคอร์ด)
    list_filter = ('project', 'created_at')

    # ฟิลด์ที่จะค้นหาได้จาก search box ด้านบน
    search_fields = ('name', 'alias', 'project__name')

    # ฟิลด์ที่ให้แสดงเป็นแบบอ่านอย่างเดียวใน admin (ไม่สามารถแก้ไขได้จาก form)
    readonly_fields = ('created_at',)

    # ให้หน้า admin แสดง navigation ตามวันที่สร้าง (ช่วยเลื่อนดูตามปี/เดือน)
    date_hierarchy = 'created_at'

    # เรียงลำดับเริ่มต้นให้แสดงล่าสุดก่อน
    ordering = ('-created_at',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('project', 'name', 'world_type', 'created_at', 'created_by')
    list_filter = ('project', 'world_type', 'created_at')
    search_fields = ('name', 'project__name')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)



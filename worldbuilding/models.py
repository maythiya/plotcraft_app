#เพื่อเก็บความสัมพันธ์แบบไม่สมมาตร (เช่น พ่อ->ลูก แต่ลูกไม่จำเป็นต้องเป็นพ่อในฟิลด์เดียวกัน)
#`portrait` เป็น `ImageField` ดังนั้นต้องติดตั้งไลบรารี `Pillow` และตั้งค่า `MEDIA_ROOT`/`MEDIA_URL`
#`project` เป็น `ForeignKey` ไปยัง `Project` (ตั้งเป็น `null=True, blank=True`) เพื่อให้สามารถเชื่อมกับโปรเจ็กต์หรือปล่อยว่างได้
#การใช้งานสั้นๆ: หลังจากแก้โมเดล ต้องรัน `makemigrations` และ `migrate` เพื่ออัพเดตฐานข้อมูล

from django.db import models
from django.conf import settings
from notes.models import Novel

class Character(models.Model):
    project = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='characters', null=True, blank=True)

    # Basic identity
    name = models.CharField(max_length=200)
    alias = models.CharField(max_length=200, blank=True)

    # Demographics
    age = models.IntegerField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    GENDER_CHOICES = [
        ('M', 'ชาย'),
        ('F', 'หญิง'),
        ('O', 'อื่นๆ'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    species = models.CharField(max_length=200, blank=True)
    role = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=100, blank=True)

    # Physical
    occupation = models.CharField(max_length=200, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    appearance = models.TextField(blank=True)

    # Personality & background
    personality = models.TextField(blank=True)
    background = models.TextField(blank=True)
    goals = models.TextField(blank=True)

    # Skills/stats
    strengths = models.TextField(blank=True)
    weaknesses = models.TextField(blank=True)
    skills = models.TextField(blank=True)

    # Location & relationships
    location = models.ForeignKey('Location', null=True, blank=True, on_delete=models.CASCADE)
    relationships = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='related_to')

    # Extra
    notes = models.TextField(blank=True)
    portrait = models.ImageField(upload_to='portraits/', null=True, blank=True)

    # บันทึกเวลาที่สร้างเรคคอร์ดนี้ไว้ในฐานข้อมูล (อ่านได้ใน admin และใช้สำหรับเรียงลำดับ)
    # auto_now_add=True จะใส่ timestamp ตอนสร้างครั้งแรกเท่านั้น
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    

    # เก็บ user ที่เป็นผู้สร้าง (ถ้ามี) เพื่อให้ทราบว่าใครเป็นผู้สร้างตัวละครนี้
    # ใช้ settings.AUTH_USER_MODEL เพื่อรองรับกรณีที่โปรเจ็กต์ใช้ custom user model
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,  # เปลี่ยนจาก SET_NULL เป็น CASCADE
        related_name='created_characters'
    )

    def __str__(self):
        return self.name
    
class Location(models.Model):
    # เชื่อมกับ Project (Note)
    project = models.ForeignKey(Novel, on_delete=models.SET_NULL, null=True, blank=True, related_name='locations')
    
    # ข้อมูลพื้นฐาน
    name = models.CharField(max_length=200)
    world_type = models.CharField(max_length=100, blank=True, help_text="Ex: Fantasy, Sci-Fi, Omegaverse")
    map_image = models.ImageField(upload_to='location_maps/', null=True, blank=True)
    
    # ความสัมพันธ์
    residents = models.ManyToManyField('Character', blank=True, related_name='resides_in')
    
    # ภูมิประเทศ
    terrain = models.TextField(blank=True, help_text="ลักษณะภูมิประเทศ")
    climate = models.TextField(blank=True, help_text="สภาพอากาศ")
    ecosystem = models.TextField(blank=True, help_text="ระบบนิเวศ")
    
    # ประวัติศาสตร์
    history = models.TextField(blank=True, help_text="ประวัติศาสตร์ความเป็นมา")
    myths = models.TextField(blank=True, help_text="ตำนานและเรื่องเล่า")
    
    # สังคม
    politics = models.TextField(blank=True, help_text="การปกครอง")
    economy = models.TextField(blank=True, help_text="ระบบเศรษฐกิจ")
    culture = models.TextField(blank=True, help_text="วัฒนธรรม ความเชื่อ ศาสนา")
    language = models.TextField(blank=True, help_text="ภาษาที่ใช้")
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    CATEGORY_CHOICES = [
        ('weapon', 'Weapon (อาวุธ)'),
        ('apparel', 'Apparel/Clothing (เครื่องแต่งกาย)'),
        ('item', 'Item/Consumable (ไอเทม/ยา)'),
        ('key_item', 'Key Item/Artifact (วัตถุสำคัญ/อาร์ติแฟกต์)'),
        ('technology', 'Technology (เทคโนโลยี)'),
        ('vehicle', 'Vehicle (ยานพาหนะ)'),
        ('other', 'Other (อื่นๆ)'),
    ]

    # Link Note (Project)
    project = models.ForeignKey(Novel, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    
    # Basic Info
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='item')
    image = models.ImageField(upload_to='items/', null=True, blank=True)
    
    # Mechanics
    abilities = models.TextField(blank=True, help_text="ความสามารถพิเศษ หรือผลของไอเทม")
    limitations = models.TextField(blank=True, help_text="เงื่อนไข ข้อจำกัด หรือผลข้างเคียง")
    
    # Lore & Description
    appearance = models.TextField(blank=True, help_text="ลักษณะภายนอก วัสดุ สี")
    history = models.TextField(blank=True, help_text="ประวัติความเป็นมา ตำนาน")
    
    # Connections
    owner = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True, blank=True, related_name='inventory', help_text="ผู้ครอบครองปัจจุบัน")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='items', help_text="สถานที่ที่เก็บซ่อนอยู่ (ถ้าไม่มีเจ้าของ)")

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

# Create your models here.

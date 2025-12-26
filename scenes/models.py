from django.conf import settings
from django.db import models
from notes.models import Novel # ดึง Novel มาเชื่อม Project
from worldbuilding.models import Character, Item, Location # ดึง Worldbuilding มาใช้

class Scene(models.Model):
    STATUS_CHOICES = [
        ('idea', 'Idea (ไอเดียร่าง)'),
        ('draft', 'Drafting (กำลังเขียน)'),
        ('revision', 'Revision (รีไรท์)'),
        ('finished', 'Finished (เสร็จสมบูรณ์)'),
    ]

    # 1. ความเชื่อมโยงหลัก
    project = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='scenes', help_text="ฉากนี้อยู่ในนิยายเรื่องไหน")
    title = models.CharField(max_length=200, verbose_name="ชื่อฉาก")
    order = models.IntegerField(default=0, verbose_name="ลำดับฉาก") # เอาไว้เรียง 1, 2, 3
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='idea')

    # 2. องค์ประกอบฉาก (Worldbuilding Elements)
    # POV: ฉากนี้เล่าผ่านมุมมองใคร (One-to-Many)
    pov_character = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True, blank=True, related_name='pov_scenes')
    # Location: เกิดที่ไหน (One-to-Many)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='scenes')
    # Characters: ใครอยู่ในฉากบ้าง (Many-to-Many)
    characters = models.ManyToManyField(Character, blank=True, related_name='appeared_in_scenes')
    # Items: ใช้อุปกรณ์อะไรบ้าง (Many-to-Many)
    items = models.ManyToManyField(Item, blank=True, related_name='used_in_scenes')

    # 3. โครงสร้างการเล่าเรื่อง (Story Structure)
    goal = models.TextField(blank=True, help_text="ตัวละครต้องการอะไรในฉากนี้?")
    conflict = models.TextField(blank=True, help_text="อุปสรรคคืออะไร?")
    outcome = models.TextField(blank=True, help_text="ผลลัพธ์เป็นอย่างไร? (ได้/ไม่ได้)")
    
    # 4. เนื้อหา
    content = models.TextField(blank=True, help_text="เนื้อหาฉาก หรือบทร่าง")

    # System fields
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at'] # เรียงตามลำดับที่กำหนดก่อน

    def __str__(self):
        return f"{self.order}. {self.title}"
# Create your models here.

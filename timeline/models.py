from django.db import models
from django.conf import settings
from notes.models import Note            
from worldbuilding.models import Character 
from scenes.models import Scene # <--- ต้อง import Scene มาด้วย

class Timeline(models.Model):
    title = models.CharField(max_length=200, default="New Timeline")
    description = models.TextField(blank=True, null=True)
    related_project = models.ForeignKey(Note, on_delete=models.SET_NULL, null=True, blank=True, related_name='timelines')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class TimelineEvent(models.Model):
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE, related_name='events')
    
    # ข้อมูลเวลา
    time_label = models.CharField(max_length=100, default="", verbose_name="ช่วงเวลา/ปี")
    
    # [เพิ่ม] ลำดับ (สำคัญมาก! ถ้าไม่มีตัวนี้ ระบบลากวางจะพัง)
    order = models.IntegerField(default=0, verbose_name="ลำดับ")
    
    # เนื้อหา
    title = models.CharField(max_length=200, default="", verbose_name="ชื่อเหตุการณ์")
    description = models.TextField(blank=True, default="", verbose_name="รายละเอียดเหตุการณ์")
    image = models.ImageField(upload_to='timeline_events/', blank=True, null=True, verbose_name="รูปภาพเหตุการณ์")
    
    # [เพิ่ม] เชื่อมกับฉาก
    related_scene = models.ForeignKey(Scene, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="ตรงกับฉาก")
    
    # ตัวละคร
    characters = models.ManyToManyField(Character, blank=True, related_name='timeline_events')

    class Meta:
        ordering = ['order'] # สั่งให้เรียงตาม order เสมอ

    def __str__(self):
        return f"{self.time_label}: {self.title}"
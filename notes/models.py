from django.db import models
from django.conf import settings

class Novel(models.Model):
    CATEGORY_CHOICES = [
        ('FANTASY', 'แฟนตาซี (Fantasy)'),
        ('BL', 'วาย (Boy Love)'),
        ('GL', 'ยูริ (Girl Love)'),
        ('ROMANCE', 'รักโรแมนติก'),
        ('SCIFI', 'ไซไฟ/อนาคต'),
        ('ACTION', 'แอคชั่น/กำลังภายใน'),
        ('HORROR', 'สยองขวัญ/ลึกลับ'),
        ('FANFIC', 'แฟนฟิคชั่น'),
        ('OTHER', 'อื่นๆ'),
    ]

    RATING_CHOICES = [
        ('G', 'ทั่วไป (General)'),
        ('PG', 'PG-13 (13+)'),
        ('R18', 'NC-18 (18+)'),
        ('R20', 'ฉ20 (20+)'),
    ]
    
    STATUS_CHOICES = [
        ('ONGOING', 'ยังไม่จบ'),
        ('COMPLETED', 'จบแล้ว'),
    ]

    title = models.CharField(max_length=200, verbose_name="ชื่อเรื่อง")
    synopsis = models.TextField(blank=True, verbose_name="คำโปรย/เรื่องย่อ")
    cover_image = models.ImageField(upload_to='novel_covers/', blank=True, null=True, verbose_name="รูปปก")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='OTHER', verbose_name="หมวดหมู่")
    rating = models.CharField(max_length=5, choices=RATING_CHOICES, default='G', verbose_name="ระดับเนื้อหา")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ONGOING', verbose_name="สถานะเรื่อง")
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='novels')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Chapter(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200, verbose_name="ชื่อตอน")
    content = models.TextField(blank=True, verbose_name="เนื้อหา")
    order = models.IntegerField(default=1, verbose_name="ลำดับตอน")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.novel.title} - {self.title}"
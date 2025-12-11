from django.db import models
from django.conf import settings


class Note(models.Model):

    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # เก็บผู้เขียนโน้ต เพื่อให้เราสามารถกรองของแต่ละผู้ใช้ได้
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='notes'
    )

    def __str__(self):
        return self.title
# Create your models here.

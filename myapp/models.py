from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)  # เพิ่มฟิลด์ birthdate
    user_status = models.CharField(max_length=50, blank=True, null=True)  # ต้องมี
    role = models.CharField(max_length=50, blank=True, null=True)  # ต้องมี
    created_at = models.DateTimeField(auto_now_add=True)  # เพิ่มฟิลด์ created_at

    display_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="ชื่อที่ใช้แสดง")
    
    # ป้องกัน reverse accessor clash
    groups = models.ManyToManyField(
        Group,
        related_name='myapp_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='myapp_user_set_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

class Project(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
# Create your models here.


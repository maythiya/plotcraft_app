# myapp/forms.py
from django.contrib.auth.models import AbstractUser
from django import forms
from .models import User, Profile # เพิ่ม Profile เข้ามาตรงนี้
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=False)
    birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "username", "email", "birthdate", "phone", "password1", "password2",
        )

# ฟอร์มสำหรับแก้ไขข้อมูล User (Email, เบอร์, ชื่อเล่น)
class UserForm(forms.ModelForm):
     class Meta:
        model = User
        fields = ['display_name', 'email', 'phone']

     def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        # แต่ง Style ให้ช่อง Input
        self.fields['display_name'].widget.attrs.update({
            'class': 'w-full px-4 py-2 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#DAA520] focus:border-[#DAA520] outline-none transition',
            'placeholder': 'ชื่อเล่น / นามแฝง'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'w-full px-4 py-2 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#DAA520] focus:border-[#DAA520] outline-none transition',
        })
        self.fields['phone'].widget.attrs.update({
            'class': 'w-full px-4 py-2 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#DAA520] focus:border-[#DAA520] outline-none transition',
        })

# --- เพิ่มส่วนนี้: ฟอร์มสำหรับ Profile (รูปภาพ และ Bio) ---
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        # แต่ง Style ให้ช่อง Bio
        self.fields['bio'].widget.attrs.update({
            'class': 'w-full px-4 py-2 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#DAA520] focus:border-[#DAA520] outline-none transition',
            'rows': '3',
            'placeholder': 'เขียนแนะนำตัวสั้นๆ...'
        })
        
        # แต่ง Style ให้ช่อง Image (FileInput)
        # หมายเหตุ: ในหน้า HTML เราอาจจะซ่อน Input นี้แล้วใช้ปุ่มสวยๆ แทน แต่ต้องมีไว้เพื่อรับค่า
        self.fields['image'].widget.attrs.update({
            'class': 'hidden', # ซ่อนไว้ เพราะเราใช้ UI สวยๆ ในหน้า HTML กดแทน
            'id': 'id_image',  # ไอดีต้องตรงกับ <label for="id_image"> ในหน้า HTML
            'accept': 'image/*' # บังคับให้เลือกได้แค่รูปภาพ
        })

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio'] # เอาแค่รูปกับ bio

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # แต่ง input ให้ซ่อนไว้ (เราจะใช้ปุ่มสวยๆ กดแทน) หรือจะโชว์ปกติก็ได้
        self.fields['image'].widget.attrs.update({'class': 'hidden', 'id': 'id_image'})
        self.fields['bio'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-[#DAA520]',
            'rows': 3,
            'placeholder': 'แนะนำตัวสั้นๆ...'
        })
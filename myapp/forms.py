# myapp/forms.py
from django.contrib.auth.models import AbstractUser
from django import forms
from .models import User
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

class UserForm(forms.ModelForm):
     class Meta:
        model = User
        fields = ['display_name', 'email', 'phone']

     def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        # แต่ง Style ให้ช่อง Display Name
        self.fields['display_name'].widget.attrs.update({
            'class': 'w-full md:w-1/2 px-4 py-2 bg-white border border-[#2F4F4F]/20 rounded-lg focus:ring-2 focus:ring-[#DAA520] focus:border-[#DAA520] focus:outline-none transition',
            'placeholder': 'ชื่อเล่น / นามแฝง'
        })


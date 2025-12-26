# คอมเมนต์อธิบายการเปลี่ยนแปลงของฟอร์ม
# - `CharacterForm` ถูกขยายให้มีฟิลด์ครบตาม `Character` model
# - เพิ่ม `project` เป็น `ModelChoiceField` เพื่อให้เลือกโปรเจ็กต์ขณะสร้างตัวละคร (ไม่บังคับ)
# - `fields` ระบุฟิลด์ที่จะแสดงในฟอร์ม (รวมถึง `portrait` สำหรับอัปโหลดรูป)
# - ใช้ `widgets` เพื่อให้ input เหมาะกับชนิดข้อมูล เช่น `DateInput` สำหรับ `birth_date` และ `Textarea` สำหรับฟิลด์ข้อความยาว
# - เมื่อใช้ฟอร์มใน view ต้องส่ง `request.FILES` ด้วย ถ้ามีการอัปโหลดรูป (portrait)

from django import forms
from notes.models import Novel
from .models import Character, Location, Item

# ---------------------------------------------------------
# Character Form
# ---------------------------------------------------------
class CharacterForm(forms.ModelForm):

    class Meta:
        model = Character
        fields = [
            'project', 'name', 'alias', 'age', 'birth_date', 'gender', 'species', 'role', 'status',
            'occupation', 'height', 'weight', 'appearance', 'personality', 'background', 'goals',
            'strengths', 'weaknesses', 'skills', 'location', 'relationships', 'notes', 'portrait'
        ]

    def __init__(self, user, *args, **kwargs):
        super(CharacterForm, self).__init__(*args, **kwargs)
        
        #กรองเอาเฉพาะ Novel (project) ของ User คนนั้น
        self.fields['project'].queryset = Novel.objects.filter(
            author=user, 
        )
        
        #กรอง Location ให้เห็นแค่ของ User
        self.fields['location'].queryset = Location.objects.filter(created_by=user)
        
        #Loop ใส่ Style ให้ทุก Input
        for field_name, field in self.fields.items():

            #1. ถ้าเป็นรูปภาพ (Portrait)
            if field_name == 'portrait':
                #Style สำหรับ File Input
                field.widget.attrs.update({
                    'class': 'w-full text-[#2F4F4F]'
                })

            #2. ถ้าเป็นวันเกิด ให้เปลี่ยนเป็นปฏิทิน (Date Picker)
            elif field_name == 'birth_date':
                field.widget = forms.DateInput(attrs={
                    'type': 'date',  # คำสั่งนี้จะเรียกปฏิทินของ Browser ออกมา
                    'class': 'w-full p-3 bg-[#FAEBD7]/20 border border-[#FAEBD7] rounded-lg text-[#2F4F4F] focus:outline-none focus:ring-2 focus:ring-[#DAA520]'
                }) 
            
            #3. ถ้าเป็นกล่องข้อความยาว (Textarea)
            elif isinstance(field.widget, forms.Textarea):
                #Style สำหรับ Textarea
                field.widget.attrs.update({
                    'class': 'w-full p-3 bg-[#FAEBD7]/20 border border-[#FAEBD7] rounded-lg text-[#2F4F4F] focus:outline-none focus:ring-2 focus:ring-[#DAA520]',
                    'rows': field.widget.attrs.get('rows', 3)
                })

            #4. ถ้าเป็น Select หลายค่า (Multiple Select)
            else:
                #Style สำหรับ Input ทั่วไป
                field.widget.attrs.update({
                    'class': 'w-full p-3 bg-[#FAEBD7]/20 border border-[#FAEBD7] rounded-lg text-[#2F4F4F] focus:outline-none focus:ring-2 focus:ring-[#DAA520]'
                })

# ---------------------------------------------------------
# Location Form
# ---------------------------------------------------------
class LocationForm(forms.ModelForm):
    
    class Meta:
        model = Location
        fields = [
            'project', 'name', 'world_type', 'map_image', 'residents',
            'terrain', 'climate', 'ecosystem',
            'history', 'myths',
            'politics', 'economy', 'culture', 'language'
        ]
        
    def __init__(self, user, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        
        #กรอง Project ให้เห็นแค่ของ User
        self.fields['project'].queryset = Novel.objects.filter(author=user)
        
        #กรอง Character ให้เห็นแค่ของ User
        self.fields['residents'].queryset = Character.objects.filter(created_by=user)
        
        #Loop ใส่ Style ให้ทุก Input
        for field_name, field in self.fields.items():
            if field_name == 'residents':
                 #Style สำหรับ Multiple Select (ถ้าใช้ default widget)
                 field.widget.attrs.update({
                    'class': 'w-full p-3 bg-[#FAEBD7]/20 border border-[#FAEBD7] rounded-lg text-[#2F4F4F] focus:outline-none focus:ring-2 focus:ring-[#DAA520] h-32'
                })
            else:
                #Style สำหรับ Input ทั่วไป
                field.widget.attrs.update({
                    'class': 'w-full p-3 bg-[#FAEBD7]/20 border border-[#FAEBD7] rounded-lg text-[#2F4F4F] focus:outline-none focus:ring-2 focus:ring-[#DAA520]'
                })
                
            #เพิ่ม Placeholder หรือ Rows สำหรับ Textarea
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'rows': 3})

# ---------------------------------------------------------
# Item Form
# ---------------------------------------------------------
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'project', 'name', 'category', 'image',
            'abilities', 'limitations', 'appearance', 'history',
            'owner', 'location'
        ]

    def __init__(self, user, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        
        # กรองข้อมูลตาม User
        self.fields['project'].queryset = Novel.objects.filter(author=user)
        self.fields['owner'].queryset = Character.objects.filter(created_by=user)
        self.fields['location'].queryset = Location.objects.filter(created_by=user)
        
        # ใส่ Style ให้เต็มกรอบ
        for field_name, field in self.fields.items():
            base_class = 'w-full p-3 bg-[#FAEBD7]/20 border border-[#FAEBD7] rounded-lg text-[#2F4F4F] focus:outline-none focus:ring-2 focus:ring-[#DAA520]'
            
            field.widget.attrs.update({'class': base_class})
            
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'rows': 3})
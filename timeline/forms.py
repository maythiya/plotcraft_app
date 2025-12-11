from django import forms
from .models import Timeline, TimelineEvent
from notes.models import Note
from worldbuilding.models import Character
from scenes.models import Scene

# ฟอร์มสร้าง Timeline (ปก)
class TimelineForm(forms.ModelForm):
    class Meta:
        model = Timeline
        fields = ['title', 'description', 'related_project']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['related_project'].queryset = Note.objects.filter(author=user)

# ฟอร์มสร้างเหตุการณ์ (ตัวนี้แหละที่ขาดไป!)
class EventForm(forms.ModelForm):
    class Meta:
        model = TimelineEvent
        fields = ['time_label', 'order', 'title', 'description', 'image', 'related_scene', 'characters']
    
    # รับ timeline เพิ่มเข้ามาใน arguments
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        timeline = kwargs.pop('timeline', None) # <--- รับตัวแปร timeline
        
        super().__init__(*args, **kwargs)
        
        if user:
            # 1. ตั้งค่าเริ่มต้น: ดึงมาทั้งหมดของ user (เผื่อ timeline ไม่ได้ผูกกับเรื่องไหน)
            scenes_qs = Scene.objects.filter(created_by=user)
            chars_qs = Character.objects.filter(created_by=user)
            
            # 2. ถ้า Timeline นี้ผูกกับนิยาย (Project) ให้กรองเหลือแค่เรื่องนั้น
            if timeline and timeline.related_project:
                # กรอง Scene ที่ project ตรงกัน
                scenes_qs = scenes_qs.filter(project=timeline.related_project)
                
                # กรอง Character ที่ project ตรงกัน 
                # (หมายเหตุ: ตรวจสอบให้แน่ใจว่าใน Model Character ใช้ชื่อ field ว่า 'project' หรือ 'note')
                # ถ้าใช้ชื่ออื่น เช่น 'related_note' ให้แก้ตรงคำว่า project
                chars_qs = chars_qs.filter(project=timeline.related_project)

            # 3. ยัดข้อมูลที่กรองแล้วใส่กลับเข้าไปในตัวเลือก
            self.fields['related_scene'].queryset = scenes_qs
            self.fields['characters'].queryset = chars_qs
        
        # Styling (เหมือนเดิม)
        base_style = "w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#DAA520] bg-gray-50 focus:bg-white transition"
        self.fields['time_label'].widget.attrs.update({'class': base_style, 'placeholder': 'เช่น 10 ปีก่อน'})
        self.fields['order'].widget.attrs.update({'class': base_style})
        self.fields['title'].widget.attrs.update({'class': base_style})
        self.fields['description'].widget.attrs.update({'class': f"{base_style} min-h-[100px]"})
        self.fields['related_scene'].widget.attrs.update({'class': base_style})
        self.fields['characters'].widget.attrs.update({'class': f"{base_style} h-32"})
        self.fields['image'].widget.attrs.update({'class': 'w-full text-sm text-gray-500'})

# (เก็บตัวนี้ไว้กัน Error เผื่อโค้ดเก่าเรียกใช้ แต่ตัวจริงคือ EventForm ด้านบน)
class TimelineEventForm(EventForm):
    pass
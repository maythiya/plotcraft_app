from notes.models import Note
from .models import Scene
from django import forms
from worldbuilding.models import Character, Item, Location


class SceneForm(forms.ModelForm):
    class Meta:
        model = Scene
        fields = [
            'project', 'title', 'status', 'order',
            'pov_character', 'location', 'characters', 'items',
            'goal', 'conflict', 'outcome', 'content'
        ]

    def __init__(self, user, *args, **kwargs):
        super(SceneForm, self).__init__(*args, **kwargs)
        
        #กรองเอาเฉพาะ Note ที่เป็นประเภท 'project' ของ User คนนั้น
        self.fields['project'].queryset = Note.objects.filter(
            author=user, 
        )

        self.fields['pov_character'].queryset = Character.objects.filter(created_by=user)
        self.fields['location'].queryset = Location.objects.filter(created_by=user)
        self.fields['characters'].queryset = Character.objects.filter(created_by=user)
        self.fields['items'].queryset = Item.objects.filter(created_by=user)
        
        # --- Styling (Tailwind) ---
        for field_name, field in self.fields.items():
            base_class = 'w-full p-3 bg-[#FAEBD7]/20 border border-[#FAEBD7] rounded-lg text-[#2F4F4F] focus:outline-none focus:ring-2 focus:ring-[#DAA520]'
            
            # กรณีเป็น Multiple Select (เช่น characters, items) ให้สูงหน่อย
            if field_name in ['characters', 'items']:
                field.widget.attrs.update({'class': f'{base_class} h-32'})
            # กรณี Textarea ให้สูง 3 บรรทัด
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': base_class, 'rows': 3})
            # กรณีปกติ
            else:
                field.widget.attrs.update({'class': base_class})
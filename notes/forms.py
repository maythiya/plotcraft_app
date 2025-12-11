from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
from django import forms
from .models import Novel, Chapter

class NovelForm(forms.ModelForm):
    class Meta:
        model = Novel
        fields = ['title', 'synopsis', 'category', 'rating', 'status', 'cover_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-lg focus:ring-[#DAA520] focus:border-[#DAA520]', 'placeholder': 'ชื่อเรื่อง...'}),
            'synopsis': forms.Textarea(attrs={'class': 'w-full p-3 border rounded-lg focus:ring-[#DAA520] focus:border-[#DAA520]', 'rows': 5, 'placeholder': 'เรื่องย่อ...'}),
            'category': forms.Select(attrs={'class': 'w-full p-3 border rounded-lg'}),
            'rating': forms.Select(attrs={'class': 'w-full p-3 border rounded-lg'}),
            'status': forms.Select(attrs={'class': 'w-full p-3 border rounded-lg'}),
            'cover_image': forms.FileInput(attrs={'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:bg-[#DAA520]/10 file:text-[#DAA520] hover:file:bg-[#DAA520]/20'}),
        }

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title', 'order', 'content']
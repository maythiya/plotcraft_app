from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Novel, Chapter
from .forms import NovelForm, ChapterForm

# 1. ชั้นหนังสือ (หน้ารวมนิยาย)
@login_required
def novel_list(request):
    novels = Novel.objects.filter(author=request.user).order_by('-updated_at')
    return render(request, 'notes/novel_list.html', {'novels': novels})

# 2. สร้างนิยายใหม่ (ปก, เรื่องย่อ, สถานะ)
@login_required
def novel_create(request):
    if request.method == 'POST':
        form = NovelForm(request.POST, request.FILES)
        if form.is_valid():
            novel = form.save(commit=False)
            novel.author = request.user
            novel.save()
            # สร้างเสร็จ เด้งไปหน้า Dashboard ของเรื่องนั้น
            return redirect('notes:novel_detail', pk=novel.id)
    else:
        form = NovelForm()
    return render(request, 'notes/novel_create.html', {'form': form})

@login_required
def novel_edit(request, pk):
    novel = get_object_or_404(Novel, pk=pk, author=request.user)
    if request.method == 'POST':
        form = NovelForm(request.POST, request.FILES, instance=novel)
        if form.is_valid():
            form.save()
            return redirect('notes:novel_detail', pk=novel.id)
    else:
        form = NovelForm(instance=novel)
    return render(request, 'notes/novel_create.html', {'form': form, 'is_edit': True})

# 3. Dashboard จัดการนิยาย (สารบัญตอน)
@login_required
def novel_detail(request, pk):
    novel = get_object_or_404(Novel, pk=pk, author=request.user)
    chapters = novel.chapters.all().order_by('order')
    return render(request, 'notes/novel_detail.html', {'novel': novel, 'chapters': chapters})

# 4. สร้างตอนใหม่ (กรอกชื่อตอน -> เด้งไปหน้าเขียน)
@login_required
def chapter_create(request, novel_id):
    novel = get_object_or_404(Novel, pk=novel_id, author=request.user)
    
    if request.method == 'POST':
        form = ChapterForm(request.POST)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.novel = novel
            chapter.save()
            # บันทึกข้อมูลเบื้องต้นเสร็จ เด้งไปหน้าเขียน (Editor)
            return redirect('notes:chapter_edit', novel_id=novel.id, chapter_id=chapter.id)
    else:
        # รันเลขตอนถัดไปให้อัตโนมัติ
        next_order = novel.chapters.count() + 1
        form = ChapterForm(initial={'order': next_order})
    
    return render(request, 'notes/chapter_create.html', {'form': form, 'novel': novel})

# 5. หน้าเขียนเนื้อหา (Editor)
@login_required
def chapter_edit(request, novel_id, chapter_id):
    novel = get_object_or_404(Novel, pk=novel_id, author=request.user)
    chapter = get_object_or_404(Chapter, pk=chapter_id, novel=novel)

    if request.method == 'POST':
        # รับค่าจาก Editor (ชื่อตอน + เนื้อหา)
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        chapter.title = title
        chapter.content = content
        chapter.save()
        
        # ถ้ากด Save ปกติ ให้กลับไปหน้า Dashboard
        return redirect('notes:novel_detail', pk=novel.id)

    return render(request, 'notes/chapter_write.html', {'novel': novel, 'chapter': chapter})

# 6. ลบตอน
@login_required
def chapter_delete(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk, novel__author=request.user)
    novel_id = chapter.novel.id
    if request.method == 'POST':
        chapter.delete()
    return redirect('notes:novel_detail', pk=novel_id)


# ลบนิยายทั้งหมด (รวมตอน)
@login_required
def novel_delete(request, pk):
    novel = get_object_or_404(Novel, pk=pk, author=request.user)
    if request.method == 'POST':
        novel.delete()
        return redirect('notes:novel_list')
    return redirect('notes:novel_detail', pk=pk)


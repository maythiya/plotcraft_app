from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden

from .models import Note

# ฟอร์มสำหรับสร้างหรือแก้ไขโน้ต
@login_required
def note_form(request, pk=None): # รับ pk (optional) เผื่อแก้ของเดิม
    
    # 1. ถ้าเป็นการ Submit Form (กดปุ่มบันทึก)
    if request.method == 'POST':
        title = request.POST.get('title', 'Untitled').strip()
        content = request.POST.get('content', '')
        note_id = request.POST.get('note_id') # รับ ID จาก Hidden Input

        if note_id:
            # แก้ไขของเดิม
            note = get_object_or_404(Note, id=note_id, author=request.user)
            note.title = title
            note.content = content
            note.save()
        else:
            # สร้างใหม่
            note = Note.objects.create(
                title=title if title else "โน้ตใหม่",
                content=content,
                author=request.user
            )
            
        return redirect('notes:note_detail', pk=note.id)

    # 2. ถ้าเป็นการเปิดหน้าเว็บ (GET)
    current_note = None
    if pk:
        current_note = get_object_or_404(Note, id=pk, author=request.user)

    # ดึงโน้ตทั้งหมดมาโชว์ที่ Sidebar
    existing_notes = Note.objects.filter(author=request.user).order_by('-updated_at')

    return render(request, 'notes/note_form.html', {
        'current_note': current_note,
        'existing_notes': existing_notes
    })

# ดูรายละเอียดโน้ต
@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, id=pk)
    return render(request, 'notes/note_detail.html', {'note': note})

# แสดงรายการโน้ต
@login_required
def note_list(request):
    notes = Note.objects.filter(author=request.user).order_by('-updated_at')
    return render(request, 'notes/note_list.html', {
        'notes': notes
    })

# ลบโน้ต
@login_required
def note_delete(request):
    """ลบโน้ตจากฐานข้อมูล

    คาดว่ามีการส่ง POST parameter `note_id` (หรือ `id`) มาจากฝั่งไคลเอ็นต์
    ตรวจสอบสิทธิ์: ผู้ใช้ต้องล็อกอินและต้องเป็นผู้เขียนโน้ตหรือเป็น staff
    ตอบกลับเป็น JSON: {'ok': True} เมื่อสำเร็จ หรือ {'error': '...'} พร้อมสถานะ HTTP ที่เหมาะสม
    """
    note_id = request.POST.get('note_id') or request.POST.get('id')
    if not note_id:
        return JsonResponse({'error': 'missing note_id'}, status=400)

    note = get_object_or_404(Note, id=note_id)

    # บังคับให้ต้องล็อกอินก่อนลบ (ป้องกันการลบโดยไม่ระบุเจ้าของ)
    if not request.user.is_authenticated:
        return HttpResponseForbidden('Authentication required')

    # ถ้ามีผู้เขียน (author) ให้ตรวจว่าเป็นเจ้าของหรือผู้ดูแล
    if note.author:
        if note.author != request.user and not request.user.is_staff:
            return HttpResponseForbidden('Permission denied')
    else:
        # ถ้าโน้ตไม่มี author (อาจสร้างก่อนที่ระบบจะบันทึกผู้เขียน) ให้อนุญาตเฉพาะ staff
        if not request.user.is_staff:
            return HttpResponseForbidden('Permission denied')

    note.delete()
    return JsonResponse({'ok': True})

# ----------------------------------------------------------------------
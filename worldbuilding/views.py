
#คอมเมนต์อธิบายการเปลี่ยนแปลงของวิว
#`character_list` ถูกแก้ให้รองรับพารามิเตอร์ GET `?project=<id>` เพื่อกรองตัวละครตามโปรเจ็กต์
#`character_create` เปลี่ยนมาใช้ `CharacterForm` เพื่อจัดการฟิลด์ทั้งหมดและการอัปโหลดไฟล์
#เมื่อเป็น POST จะรับ `request.POST` และ `request.FILES` แล้วตรวจ `form.is_valid()` ก่อนบันทึก
#บันทึกสำเร็จแล้ว redirect ไปยัง `character_list`
#`character_edit` ตอนนี้เป็น placeholder ที่ redirect กลับไปยัง list (สามารถขยายเป็นการแก้ไขตัวละครทีละตัวได้ต่อ)
#หมายเหตุ: ถ้าใช้ `ImageField` ต้องตั้งค่า `MEDIA_ROOT` และ `MEDIA_URL` ใน settings และติดตั้ง `Pillow`

from django.shortcuts import render, get_object_or_404, redirect

from .models import Character, Item, Location
from .forms import CharacterForm, ItemForm, LocationForm

from myapp.models import Project
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from notes.models import Note  # ใช้สำหรับดึง Project/Note ในการ Pre-select


def overview(request):
    return render(request, "worldbuilding/overview.html")


# ----------------------------------------------------------------------
# View: character_list (แก้ไขปัญหาการกรองข้อมูล)
# ----------------------------------------------------------------------
@login_required # ต้องล็อกอินก่อนเข้าถึง
def character_list(request):
    """List characters. Optional `project` GET parameter filters by project id, AND filters by current user."""
    
    # 1. Base Query: กรองตัวละครที่สร้างโดยผู้ใช้ปัจจุบันเท่านั้น (แก้ไขปัญหา Data Leakage)
    base_characters = Character.objects.filter(created_by=request.user)
    
    project_id = request.GET.get('project')
    if project_id:
        project = get_object_or_404(Project, id=project_id)
        # กรองตัวละครของ project นั้นๆ ที่ผู้ใช้ปัจจุบันสร้าง
        characters = base_characters.filter(project=project)
    else:
        # ใช้ตัวละครทั้งหมดที่ผู้ใช้ปัจจุบันสร้าง
        characters = base_characters.order_by('-created_at') # จัดเรียงตามเวลาสร้างล่าสุด

    return render(request, 'worldbuilding/character_list.html', {
        'characters': characters,
    })

# ----------------------------------------------------------------------
# View: character_create (แก้ไขปัญหาการใช้ฟอร์มและอัปโหลดไฟล์)
# ----------------------------------------------------------------------
@login_required
def character_create(request):
    if request.method == 'POST':
        form = CharacterForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            # บันทึกแบบยังไม่ commit เพื่อให้สามารถตั้งค่า `created_by` ก่อน save ได้
            character = form.save(commit=False)
            if request.user.is_authenticated:
                character.created_by = request.user
            character.save()
            form.save_m2m()
            # หลังจากบันทึก ให้ไปที่หน้ารายละเอียดของตัวละคร (read-only)
            return redirect('worldbuilding:character_detail', character.id)
    else:
        # allow passing ?project=<id> to preselect project
        initial = {}
        project_id = request.GET.get('project')
        if project_id:
            try:
                initial['project'] = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                pass
        form = CharacterForm(request.user, initial=initial)
    return render(request, 'worldbuilding/character_form.html', {'form': form})

# ----------------------------------------------------------------------
# View: character_edit (แก้ไขปัญหาการลบและ Redirect)
# ----------------------------------------------------------------------
@login_required
def character_edit(request, pk):
    character = get_object_or_404(Character, id=pk) 
    
    #ตรวจสอบสิทธิ์การแก้ไข/ลบ
    if character.created_by != request.user:
        messages.error(request, "คุณไม่มีสิทธิ์แก้ไข/ลบตัวละครนี้")
        return redirect('worldbuilding:character_detail', pk=pk)

    if request.method == 'POST':
        
        #ตรวจสอบ Delete Action เป็นอันดับแรกสุด (สำคัญมาก)
        if "character_delete" in request.POST:
            character_name = character.name
            character.delete() # ลบตัวละครออกจาก Database
            messages.success(request, f"ลบตัวละคร '{character_name}' เรียบร้อยแล้ว")
            return redirect('worldbuilding:character_list') # <<< Redirect ไปที่หน้า List
        
        #ถ้าไม่ใช่ Delete ให้ประมวลผลการบันทึก/แก้ไขฟอร์มตามปกติ
        form = CharacterForm(request.user, request.POST, request.FILES, instance=character)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user #ยืนยันว่าผู้สร้างคือผู้ใช้ปัจจุบัน
            obj.save()
            form.save_m2m()
            messages.success(request, f"บันทึกตัวละคร '{obj.name}' เรียบร้อยแล้ว")
            return redirect('worldbuilding:character_detail', pk=obj.id)
        
    else:
        form = CharacterForm(request.user, instance=character)

    return render(request, 'worldbuilding/character_form.html', {
        'form': form,
        'character': character,
    })

# ----------------------------------------------------------------------
# View: character_detail (แก้ไขปัญหาการกรองข้อมูล)
# ----------------------------------------------------------------------
@login_required
def character_detail(request, pk):
    """แสดงรายละเอียดตัวละครในรูปแบบการ์ด (อ่านอย่างเดียว)

    - pk: primary key ของตัวละคร
    - คืนค่า template `character_detail.html` พร้อม context `character`
    """
    character = get_object_or_404(Character, id=pk)
    return render(request, 'worldbuilding/character_detail.html', {'character': character})

# ----------------------------------------------------------------------
# View: location_create (สร้างสถานที่)
# ----------------------------------------------------------------------
@login_required
def location_create(request):
    if request.method == 'POST':
        # ส่ง request.user เข้าไปเป็น argument แรกตามที่เราแก้ใน forms.py
        form = LocationForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            location = form.save(commit=False)
            location.created_by = request.user
            location.save()
            form.save_m2m() # บันทึกความสัมพันธ์ ManyToMany (เช่น residents)
            messages.success(request, f"สร้างสถานที่ '{location.name}' เรียบร้อยแล้ว")
            return redirect('worldbuilding:location_detail', pk=location.id)
    else:
        # รองรับการส่ง ?project=<id> มาทาง URL เพื่อเลือก Project อัตโนมัติ
        initial = {}
        project_id = request.GET.get('project')
        if project_id:
            try:
                # ตรวจสอบด้วยว่า Note นั้นเป็นของ User จริงๆ
                initial['project'] = Note.objects.get(id=project_id, author=request.user)
            except Note.DoesNotExist:
                pass
        
        # ส่ง request.user เข้าไปเพื่อกรอง Dropdown
        form = LocationForm(request.user, initial=initial)

    return render(request, 'worldbuilding/location_form.html', {'form': form})

# ----------------------------------------------------------------------
# View: location_edit (แก้ไขและลบสถานที่)
# ----------------------------------------------------------------------
@login_required
def location_edit(request, pk):
    location = get_object_or_404(Location, id=pk)

    # ตรวจสอบสิทธิ์ว่าเป็นเจ้าของหรือไม่
    if location.created_by != request.user:
        messages.error(request, "คุณไม่มีสิทธิ์แก้ไขสถานที่นี้")
        return redirect('worldbuilding:location_detail', pk=pk)

    if request.method == 'POST':
        
        # ตรวจสอบ Delete Action (ปุ่มลบใน location_form.html ต้องชื่อ name="location_delete")
        if "location_delete" in request.POST:
            location_name = location.name
            location.delete()
            messages.success(request, f"ลบสถานที่ '{location_name}' เรียบร้อยแล้ว")
            return redirect('worldbuilding:location_list') # Redirect ไปหน้ารายการ
        
        # ถ้าไม่ใช่การลบ ให้ทำการบันทึก
        form = LocationForm(request.user, request.POST, request.FILES, instance=location)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            form.save_m2m()
            messages.success(request, f"บันทึกข้อมูลสถานที่ '{obj.name}' เรียบร้อยแล้ว")
            return redirect('worldbuilding:location_detail', pk=obj.id)
    
    else:
        form = LocationForm(request.user, instance=location)

    return render(request, 'worldbuilding/location_form.html', {
        'form': form,
        'location': location, # ส่ง object ไปด้วยเพื่อให้รู้ว่าเป็นโหมดแก้ไข
    })

# ----------------------------------------------------------------------
# View: location_detail (แสดงรายละเอียดสถานที่)
# ----------------------------------------------------------------------
@login_required
def location_detail(request, pk):
    """แสดงรายละเอียดสถานที่"""
    location = get_object_or_404(Location, id=pk)
    
    # (Optional) ถ้าต้องการป้องกันไม่ให้คนอื่นดูสถานที่ของผู้ใช้คนอื่น
    # if location.created_by != request.user:
    #     messages.error(request, "คุณไม่มีสิทธิ์เข้าถึงสถานที่นี้")
    #     return redirect('worldbuilding:location_list')

    return render(request, 'worldbuilding/location_detail.html', {'location': location})

# ----------------------------------------------------------------------
# View: location_list (แสดงรายการสถานที่)
# ----------------------------------------------------------------------
@login_required
def location_list(request):
    """แสดงรายการสถานที่ทั้งหมดที่ผู้ใช้สร้าง"""
    locations = Location.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'worldbuilding/location_list.html', {'locations': locations})

# ----------------------------------------------------------------------
# View: item_list
# ----------------------------------------------------------------------
@login_required
def item_list(request):
    """แสดงรายการไอเท็มทั้งหมดที่ผู้ใช้สร้าง"""
    items = Item.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'worldbuilding/item_list.html', {'items': items})

# ----------------------------------------------------------------------
# View: item_detail
# ----------------------------------------------------------------------
@login_required
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'worldbuilding/item_detail.html', {'item': item})

# ----------------------------------------------------------------------
# View: item_create
# ----------------------------------------------------------------------
@login_required
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            form.save_m2m()
            messages.success(request, f"สร้างไอเทม '{item.name}' เรียบร้อยแล้ว")
            return redirect('worldbuilding:item_detail', pk=item.id)
    else:
        initial = {}
        project_id = request.GET.get('project')
        if project_id:
            try:
                initial['project'] = Note.objects.get(id=project_id, author=request.user)
            except Note.DoesNotExist:
                pass
        form = ItemForm(request.user, initial=initial)

    return render(request, 'worldbuilding/item_form.html', {'form': form})

# ----------------------------------------------------------------------
# View: item_edit
# ----------------------------------------------------------------------
@login_required
def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if item.created_by != request.user:
        # handle permission error
        return redirect('worldbuilding:item_list')

    if request.method == 'POST':
        if "item_delete" in request.POST:
            item.delete()
            return redirect('worldbuilding:item_list')
            
        form = ItemForm(request.user, request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('worldbuilding:item_detail', pk=item.id)
    else:
        form = ItemForm(request.user, instance=item)

    return render(request, 'worldbuilding/item_form.html', {'form': form, 'item': item})
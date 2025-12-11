from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from notes.models import Note
from .forms import SceneForm
from .models import Scene

# ----------------------------------------------------------------------
# View: scene_list
# ----------------------------------------------------------------------
@login_required
def scene_list(request):
    # 1. ดึง Project (Note) ทั้งหมดของผู้ใช้ เพื่อเอาไปทำปุ่มเลือก
    projects = Note.objects.filter(author=request.user)
    
    # 2. เริ่มต้นดึงฉากทั้งหมดมาก่อน
    scenes = Scene.objects.filter(created_by=request.user).order_by('order')
    
    # 3. ตรวจสอบว่ามีการเลือก Project มาไหม? (จาก URL ?project=...)
    selected_project_id = request.GET.get('project')
    selected_project = None

    if selected_project_id:
        # ถ้าเลือกมา ให้กรองเอาเฉพาะฉากของเรื่องนั้น
        scenes = scenes.filter(project_id=selected_project_id)
        # ดึงชื่อเรื่องมาแสดงหัวข้อด้วย (ถ้าหาเจอ)
        if projects.filter(id=selected_project_id).exists():
            selected_project = projects.get(id=selected_project_id)

    context = {
        'scenes': scenes,
        'projects': projects,
        'selected_project': selected_project, # ส่งข้อมูลเรื่องที่เลือกไปด้วย
    }
    return render(request, 'scenes/scene_list.html', context)

# ----------------------------------------------------------------------
# View: scene_create
# ----------------------------------------------------------------------
@login_required
def scene_create(request):
    if request.method == 'POST':
        form = SceneForm(request.user, request.POST) # ส่ง user ไปกรอง dropdown
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            form.save_m2m() #สำคัญ! เพราะมี ManyToMany (characters, items)
            messages.success(request, f"สร้างฉาก '{obj.title}' เรียบร้อย")
            return redirect(f"/scenes/?project={obj.project.id}")
    else:
        #(Optional) Auto-fill project ถ้าส่ง ?project_id= มา
        initial = {}
        if 'project' in request.GET:
             #logic ตรวจสอบความเป็นเจ้าของ project ใส่เพิ่มตรงนี้ได้
             pass
        form = SceneForm(request.user, initial=initial)

    return render(request, 'scenes/scene_form.html', {'form': form})

# ----------------------------------------------------------------------
# View: scene_edit
# ----------------------------------------------------------------------
@login_required
def scene_edit(request, pk):
    scene = get_object_or_404(Scene, pk=pk)

    # ตรวจสอบสิทธิ์
    if scene.created_by != request.user:
        messages.error(request, "ไม่มีสิทธิ์แก้ไข")
        return redirect('scenes:scene_list')

    if request.method == 'POST':
        # เก็บ project_id ไว้ก่อนลบ เพื่อใช้ redirect
        project_id = scene.project.id if scene.project else None
        
        if "scene_delete" in request.POST:
            scene.delete()
            messages.success(request, "ลบฉากเรียบร้อย")
            # ลบเสร็จ กลับไปหน้าเรื่องเดิม
            if project_id:
                return redirect(f"/scenes/?project={project_id}")
            return redirect('scenes:scene_list')

        form = SceneForm(request.user, request.POST, instance=scene)
        if form.is_valid():
            form.save()
            messages.success(request, "บันทึกฉากเรียบร้อย")
            # บันทึกเสร็จ กลับไปหน้าเรื่องเดิม
            if scene.project:
                return redirect(f"/scenes/?project={scene.project.id}")
            return redirect('scenes:scene_list')
    else:
        form = SceneForm(request.user, instance=scene)

    return render(request, 'scenes/scene_form.html', {'form': form, 'scene': scene})

# Create your views here.

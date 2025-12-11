from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.db.models import Q

from worldbuilding.models import Character, Location, Item
from notes.models import Note
from scenes.models import Scene
from timeline.models import TimelineEvent

from .forms import UserForm, RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def landing(request):
    return render(request, 'landing.html')

def home(request):
    # แสดงหน้า home พร้อมตัวอย่างการ์ดตัวละครที่ผู้ใช้สร้างไว้ (หรือการ์ดล่าสุด)
    # แสดงรายการล่าสุด 3 รายการ (ลดขนาดหน้าแรกให้กระชับ)
    max_items = 3
    if request.user.is_authenticated:
        characters = Character.objects.filter(created_by=request.user).order_by('-created_at')[:max_items]
        notes = Note.objects.filter(author=request.user).order_by('-created_at')[:max_items]
        locations = Location.objects.filter(created_by=request.user).order_by('-created_at')[:max_items]
    else:
        characters = Character.objects.all().order_by('-created_at')[:max_items]
        notes = Note.objects.all().order_by('-created_at')[:max_items]
        locations = Location.objects.all().order_by('-created_at')[:max_items]

    return render(request, 'home.html', {
        'characters': characters,
        'notes': notes,
        'locations': locations,
    })

def register(request):
    #if request.user.is_authenticated: # ===== if you open web is remember you if you logined
        #return redirect('landing')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')

        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    user = request.user

    if request.method == "POST":
        # 1. เช็คเรื่องการลบบัญชีก่อน (เพราะถ้าลบแล้วไม่ต้องทำอย่างอื่น)
        if "delete_account" in request.POST:
            user.delete()
            logout(request)
            return redirect("landing")

        # 2. [แก้ตรงนี้] สร้างตัวแปร form รอไว้เลย สำหรับทุกกรณีที่เป็น POST
        # เพื่อป้องกัน UnboundLocalError
        form = UserForm(request.POST, instance=user)

        # 3. เช็คว่ากดปุ่ม save หรือไม่
        if "save_changes" in request.POST:
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect("profile")
            
    else:
        # กรณีเป็น GET request
        form = UserForm(instance=user)

    return render(request, "profile.html", {
        "form": form,
    })

@login_required
def global_search(request):
    query = request.GET.get('q', '') # รับคำค้นหามา
    results = {}
    
    if query:
        # 1. ค้นหาใน โปรเจกต์ (Notes)
        results['projects'] = Note.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            author=request.user
        )

        # 2. ค้นหาใน ตัวละคร (Characters)
        results['characters'] = Character.objects.filter(
            Q(name__icontains=query) | 
            Q(background__icontains=query) | 
            Q(personality__icontains=query) |
            Q(appearance__icontains=query) |
            Q(alias__icontains=query),
            created_by=request.user
        )

        # 3. ค้นหาใน ฉาก (Scenes)
        results['scenes'] = Scene.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query),
            created_by=request.user
        )

        # 4. ค้นหาใน Timeline (Events)
        results['timeline_events'] = TimelineEvent.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query),
            timeline__created_by=request.user
        )

        # 5. ค้นหาใน สถานที่ (Locations)
        # Location model ไม่มีฟิลด์ `description` ดังนั้นค้นหาในฟิลด์ข้อความที่มีจริงแทน
        results['locations'] = Location.objects.filter(
            Q(name__icontains=query) |
            Q(history__icontains=query) |
            Q(terrain__icontains=query) |
            Q(climate__icontains=query) |
            Q(ecosystem__icontains=query) |
            Q(myths__icontains=query) |
            Q(culture__icontains=query) |
            Q(politics__icontains=query) |
            Q(economy__icontains=query) |
            Q(language__icontains=query),
            created_by=request.user
        )

        # 6. ค้นหาใน ไอเท็ม (Items)
        # Item model ไม่มีฟิลด์ `description` — ใช้ฟิลด์ที่มีแทน (appearance, history, abilities, limitations)
        results['items'] = Item.objects.filter(
            Q(name__icontains=query) |
            Q(appearance__icontains=query) |
            Q(history__icontains=query) |
            Q(abilities__icontains=query) |
            Q(limitations__icontains=query),
            created_by=request.user
        )

    return render(request, 'search_results.html', {'query': query, 'results': results})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.db.models import Q

from worldbuilding.models import Character, Location, Item
from notes.models import Novel
from scenes.models import Scene
from timeline.models import TimelineEvent

from .forms import UserForm, RegisterForm, ProfileForm
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
        novels = Novel.objects.filter(author=request.user).order_by('-updated_at')[:max_items]
        locations = Location.objects.filter(created_by=request.user).order_by('-created_at')[:max_items]
    else:
        characters = Character.objects.all().order_by('-created_at')[:max_items]
        novels = Novel.objects.all().order_by('-updated_at')[:max_items]
        locations = Location.objects.all().order_by('-created_at')[:max_items]

    return render(request, 'home.html', {
        'characters': characters,
        'novels': novels,
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
    if request.method == 'POST':
        if 'delete_account' in request.POST:
            user = request.user
            logout(request)
            user.delete()
            return redirect('landing')

        # รับข้อมูลทั้ง 2 ฟอร์ม
        u_form = UserForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile) # เพิ่ม request.FILES

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'บันทึกข้อมูลสำเร็จ')
            return redirect('profile')
    else:
        u_form = UserForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)

    # ส่งทั้ง u_form และ p_form ไปที่หน้าเว็บ
    return render(request, 'profile.html', {'u_form': u_form, 'p_form': p_form})

@login_required
def global_search(request):
    query = request.GET.get('q', '') # รับคำค้นหามา
    results = {}
    
    if query:
        # 1. ค้นหาใน โปรเจกต์ (Novels)
        results['projects'] = Novel.objects.filter(
            Q(title__icontains=query) | Q(synopsis__icontains=query),
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



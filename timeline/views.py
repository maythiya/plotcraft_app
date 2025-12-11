from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Timeline, TimelineEvent
from .forms import TimelineForm, TimelineEventForm, EventForm
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
import json


def timeline_list(request):
    """List all timelines (or user's timelines)."""
    if request.user.is_authenticated:
        timelines = Timeline.objects.filter(created_by=request.user).order_by('-updated_at')
    else:
        timelines = Timeline.objects.all().order_by('-updated_at')
    return render(request, 'timeline/timeline_list.html', {'timelines': timelines})


@login_required
def timeline_create(request):
    if request.method == 'POST':
        # [จุดสำคัญ] ต้องใช้ TimelineForm
        form = TimelineForm(request.POST, user=request.user) 
        
        if form.is_valid():
            timeline = form.save(commit=False)
            timeline.created_by = request.user
            timeline.save()
            # บันทึกเสร็จแล้ว ดีดไปหน้า timeline_detail
            return redirect('timeline:timeline_detail', pk=timeline.id)
    else:
        form = TimelineForm(user=request.user)
    
    return render(request, 'timeline/timeline_form.html', {'form': form})


def timeline_detail(request, pk):
    timeline = get_object_or_404(Timeline, id=pk)
    events = timeline.events.all().order_by('order')

    # [แก้] ใช้ EventForm (ที่มี css สวยๆ) แทน TimelineEventForm ธรรมดา
    # และใส่ request.user เพื่อให้มันกรองฉาก/ตัวละครของ user คนนั้น
    if request.user.is_authenticated:
        event_form = EventForm(user=request.user, timeline=timeline)
    else:
        event_form = EventForm() # Fallback

    return render(request, 'timeline/timeline_detail.html', {
        'timeline': timeline,
        'events': events,
        'event_form': event_form, # ส่งไปให้หน้าเว็บใช้
    })


@login_required
def timeline_delete(request, pk):
    timeline = get_object_or_404(Timeline, id=pk)
    if timeline.created_by != request.user and not request.user.is_staff:
        return HttpResponseForbidden()
    if request.method == 'POST':
        timeline.delete()
        return redirect('timeline:timeline_list')
    return render(request, 'timeline/timeline_confirm_delete.html', {'timeline': timeline})


@require_POST
def update_event_order(request):
    try:
        data = json.loads(request.body)
        event_ids = data.get('ids', [])
        for index, event_id in enumerate(event_ids):
            # เรียงลำดับใหม่
            TimelineEvent.objects.filter(
                id=event_id, 
                timeline__created_by=request.user
            ).update(order=index)
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error'}, status=400)
    
@login_required
def timeline_event_create(request, pk):
    timeline = get_object_or_404(Timeline, id=pk)
    
    # เช็คว่าเป็นเจ้าของ Timeline หรือไม่
    if timeline.created_by != request.user and not request.user.is_staff:
        return HttpResponseForbidden()

    if request.method == 'POST':
        # [จุดที่แก้] ต้องใส่ 3 อย่างนี้ให้ครบ:
        # 1. request.POST (ข้อมูลตัวหนังสือ)
        # 2. request.FILES (รูปภาพ - ถ้าลืมอันนี้ รูปจะไม่มา)
        # 3. user=request.user (เพื่อให้ฟอร์มรู้ว่าเป็นของใคร)
        form = EventForm(request.POST, request.FILES, user=request.user, timeline=timeline)
        
        if form.is_valid():
            ev = form.save(commit=False)
            ev.timeline = timeline
            ev.save()
            form.save_m2m() # บันทึกตัวละครที่เลือก
            print("✅ บันทึกสำเร็จ!")
            return redirect('timeline:timeline_detail', pk=timeline.id)
        else:
            # [จุดสำคัญ] ถ้าไม่ผ่าน ให้ปริ้น Error ออกมาดูใน Terminal (จอดำๆ)
            print("❌ Form Error:", form.errors)
            
    # ถ้าไม่ใช่ POST หรือ Error ให้กลับไปหน้าเดิม
    return redirect('timeline:timeline_detail', pk=timeline.id)


@login_required
def timeline_event_update(request, pk):
    event = get_object_or_404(TimelineEvent, pk=pk)
    timeline = event.timeline
    
    # เช็คสิทธิ์เจ้าของ
    if event.timeline.created_by != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        # ใช้ instance=event เพื่อบอกว่านี่คือการแก้ไขของเดิม
        form = EventForm(request.POST, request.FILES, instance=event, user=request.user, timeline=timeline)
        if form.is_valid():
            form.save()
            return redirect('timeline:timeline_detail', pk=event.timeline.id)
    
    return redirect('timeline:timeline_detail', pk=event.timeline.id)

@login_required
def timeline_event_delete(request, pk):
    """ฟังก์ชันสำหรับลบเหตุการณ์"""
    event = get_object_or_404(TimelineEvent, pk=pk)
    timeline_id = event.timeline.id
    
    if event.timeline.created_by == request.user:
        if request.method == 'POST':
            event.delete()
            
    return redirect('timeline:timeline_detail', pk=timeline_id)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Sum, Q
from datetime import date, timedelta
import json

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import PickupSchedule, Appointment, WasteCollector, Zone
from .forms import PickupScheduleForm, AppointmentForm, ScheduleStatusForm, AppointmentStatusForm

@login_required
def dashboard(request):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    # Core stats
    total_schedules = PickupSchedule.objects.count()
    today_schedules = PickupSchedule.objects.filter(scheduled_date=today)
    week_schedules = PickupSchedule.objects.filter(scheduled_date__range=[week_start, week_end])
    completed_today = today_schedules.filter(status='completed').count()
    pending_appointments = Appointment.objects.filter(status='pending').count()
    active_collectors = WasteCollector.objects.filter(active=True).count()

    # Waste collected this week
    waste_this_week = week_schedules.filter(status='completed').aggregate(
        total=Sum('actual_kg'))['total'] or 0

    # Recent schedules
    recent_schedules = PickupSchedule.objects.select_related('zone', 'collector')[:6]

    # Upcoming appointments
    upcoming_appointments = Appointment.objects.filter(
        appointment_date__gte=today,
        status__in=['pending', 'confirmed']
    ).select_related('zone')[:5]

    # Zone activity for chart (last 7 days)
    zones = Zone.objects.filter(active=True)
    zone_data = []
    for zone in zones:
        count = PickupSchedule.objects.filter(
            zone=zone,
            scheduled_date__range=[week_start, week_end]
        ).count()
        zone_data.append({'name': zone.name, 'count': count, 'color': zone.color})

    # Weekly pickup trend (last 4 weeks)
    weekly_trend = []
    for i in range(3, -1, -1):
        ws = today - timedelta(weeks=i, days=today.weekday())
        we = ws + timedelta(days=6)
        completed = PickupSchedule.objects.filter(
            scheduled_date__range=[ws, we], status='completed').count()
        missed = PickupSchedule.objects.filter(
            scheduled_date__range=[ws, we], status='missed').count()
        weekly_trend.append({
            'week': f"Wk {4-i}",
            'completed': completed,
            'missed': missed,
        })

    context = {
        'today': today,
        'total_schedules': total_schedules,
        'today_count': today_schedules.count(),
        'completed_today': completed_today,
        'pending_appointments': pending_appointments,
        'active_collectors': active_collectors,
        'waste_this_week': round(float(waste_this_week), 1),
        'recent_schedules': recent_schedules,
        'upcoming_appointments': upcoming_appointments,
        'zone_data_json': json.dumps(zone_data),
        'weekly_trend_json': json.dumps(weekly_trend),
        'completion_rate': round((completed_today / today_schedules.count() * 100) if today_schedules.count() > 0 else 0),
    }
    return render(request, 'scheduling/dashboard.html', context)


# ── SCHEDULES ──────────────────────────────────────────────────────────────────
@login_required
def schedule_list(request):
    qs = PickupSchedule.objects.select_related('zone', 'collector')

    status_filter = request.GET.get('status', '')
    zone_filter = request.GET.get('zone', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    if status_filter:
        qs = qs.filter(status=status_filter)
    if zone_filter:
        qs = qs.filter(zone_id=zone_filter)
    if date_from:
        qs = qs.filter(scheduled_date__gte=date_from)
    if date_to:
        qs = qs.filter(scheduled_date__lte=date_to)

    context = {
        'schedules': qs[:50],
        'zones': Zone.objects.filter(active=True),
        'status_choices': PickupSchedule.STATUS_CHOICES,
        'filters': {'status': status_filter, 'zone': zone_filter, 'date_from': date_from, 'date_to': date_to},
    }
    return render(request, 'scheduling/schedule_list.html', context)

@login_required
def schedule_create(request):
    if request.method == 'POST':
        form = PickupScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            if request.user.is_authenticated:
                schedule.created_by = request.user
            schedule.save()
            messages.success(request, f'Schedule "{schedule.title}" created successfully.')
            return redirect('schedule_list')
    else:
        form = PickupScheduleForm()
    return render(request, 'scheduling/schedule_form.html', {'form': form, 'action': 'Create'})

@login_required
def schedule_detail(request, pk):
    schedule = get_object_or_404(PickupSchedule.objects.select_related('zone', 'collector'), pk=pk)
    status_form = ScheduleStatusForm(instance=schedule)
    if request.method == 'POST':
        status_form = ScheduleStatusForm(request.POST, instance=schedule)
        if status_form.is_valid():
            status_form.save()
            messages.success(request, 'Schedule updated.')
            return redirect('schedule_detail', pk=pk)
    return render(request, 'scheduling/schedule_detail.html', {'schedule': schedule, 'status_form': status_form})

@login_required
def schedule_delete(request, pk):
    schedule = get_object_or_404(PickupSchedule, pk=pk)
    if request.method == 'POST':
        title = schedule.title
        schedule.delete()
        messages.success(request, f'Schedule "{title}" deleted.')
        return redirect('schedule_list')
    return render(request, 'scheduling/confirm_delete.html', {'object': schedule, 'type': 'Schedule'})


# ── APPOINTMENTS ───────────────────────────────────────────────────────────────
@login_required
def appointment_list(request):
    qs = Appointment.objects.select_related('zone', 'assigned_collector')
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    context = {
        'appointments': qs[:50],
        'status_choices': Appointment.STATUS_CHOICES,
        'filters': {'status': status_filter},
    }
    return render(request, 'scheduling/appointment_list.html', context)

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save()
            messages.success(request, f'Appointment booked! Reference: {appt.reference_code}')
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'scheduling/appointment_form.html', {'form': form, 'action': 'Book'})

@login_required
def appointment_detail(request, pk):
    appt = get_object_or_404(Appointment.objects.select_related('zone', 'assigned_collector'), pk=pk)
    status_form = AppointmentStatusForm(instance=appt)
    if request.method == 'POST':
        status_form = AppointmentStatusForm(request.POST, instance=appt)
        if status_form.is_valid():
            status_form.save()
            messages.success(request, 'Appointment updated.')
            return redirect('appointment_detail', pk=pk)
    return render(request, 'scheduling/appointment_detail.html', {'appt': appt, 'status_form': status_form})


# ── COLLECTORS ─────────────────────────────────────────────────────────────────
@login_required
def collector_list(request):
    collectors = WasteCollector.objects.select_related('zone').annotate(
        total_schedules=Count('schedules'),
        completed=Count('schedules', filter=Q(schedules__status='completed'))
    )
    return render(request, 'scheduling/collector_list.html', {'collectors': collectors})


# ── ZONES ──────────────────────────────────────────────────────────────────────
@login_required
def zone_list(request):
    zones = Zone.objects.annotate(
        total_schedules=Count('schedules'),
        active_collectors=Count('collectors', filter=Q(collectors__active=True))
    )
    return render(request, 'scheduling/zone_list.html', {'zones': zones})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created! Welcome to CleanCity.')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'scheduling/register.html', {'form': form})

@login_required
def about(request):
    return render(request, 'scheduling/about.html')


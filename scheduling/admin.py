from django.contrib import admin
from .models import Zone, WasteCollector, PickupSchedule, Appointment, DashboardStat


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'area', 'lga', 'active']
    list_filter = ['active', 'lga']


@admin.register(WasteCollector)
class WasteCollectorAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'vehicle_number', 'vehicle_type', 'zone', 'active']
    list_filter = ['active', 'vehicle_type', 'zone']


@admin.register(PickupSchedule)
class PickupScheduleAdmin(admin.ModelAdmin):
    list_display = ['title', 'zone', 'collector', 'scheduled_date', 'scheduled_time', 'status', 'frequency']
    list_filter = ['status', 'frequency', 'zone']
    date_hierarchy = 'scheduled_date'


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['reference_code', 'resident_name', 'appointment_type', 'appointment_date', 'status', 'zone']
    list_filter = ['status', 'appointment_type', 'zone']
    readonly_fields = ['reference_code']
    date_hierarchy = 'appointment_date'


@admin.register(DashboardStat)
class DashboardStatAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_pickups', 'completed_pickups', 'total_waste_kg']

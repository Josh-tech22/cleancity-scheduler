from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Zone(models.Model):
    name = models.CharField(max_length=100)
    area = models.CharField(max_length=200)
    lga = models.CharField(max_length=100, default='Port Harcourt')
    color = models.CharField(max_length=7, default='#2ecc71')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.area}"

    class Meta:
        ordering = ['name']


class WasteCollector(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    vehicle_number = models.CharField(max_length=30)
    vehicle_type = models.CharField(max_length=50, choices=[
        ('truck', 'Waste Truck'),
        ('tricycle', 'Tricycle'),
        ('van', 'Van'),
    ], default='truck')
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True, related_name='collectors')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.vehicle_number})"

    class Meta:
        ordering = ['name']


class PickupSchedule(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('missed', 'Missed'),
        ('cancelled', 'Cancelled'),
    ]
    FREQUENCY_CHOICES = [
        ('once', 'One-time'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('biweekly', 'Bi-weekly'),
    ]

    title = models.CharField(max_length=200)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='schedules')
    collector = models.ForeignKey(WasteCollector, on_delete=models.SET_NULL, null=True, related_name='schedules')
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='weekly')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    estimated_kg = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    actual_kg = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_schedules')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} — {self.scheduled_date} ({self.zone})"

    class Meta:
        ordering = ['-scheduled_date', '-scheduled_time']


class Appointment(models.Model):
    APPOINTMENT_TYPES = [
        ('bulk', 'Bulk Waste Pickup'),
        ('hazardous', 'Hazardous Waste'),
        ('recycling', 'Recycling Collection'),
        ('complaint', 'Complaint/Inspection'),
        ('special', 'Special Request'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    resident_name = models.CharField(max_length=150)
    resident_phone = models.CharField(max_length=20)
    resident_email = models.EmailField(blank=True)
    address = models.TextField()
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True, related_name='appointments')
    appointment_type = models.CharField(max_length=30, choices=APPOINTMENT_TYPES)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_collector = models.ForeignKey(WasteCollector, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    reference_code = models.CharField(max_length=12, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.reference_code:
            import random, string
            self.reference_code = 'CC' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference_code} — {self.resident_name} ({self.appointment_date})"

    class Meta:
        ordering = ['-appointment_date', '-appointment_time']


class DashboardStat(models.Model):
    """Cached daily stats for dashboard"""
    date = models.DateField(unique=True)
    total_pickups = models.IntegerField(default=0)
    completed_pickups = models.IntegerField(default=0)
    missed_pickups = models.IntegerField(default=0)
    total_waste_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    active_collectors = models.IntegerField(default=0)
    pending_appointments = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Stats for {self.date}"

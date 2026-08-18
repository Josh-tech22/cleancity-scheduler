from django import forms
from .models import PickupSchedule, Appointment, WasteCollector, Zone


class PickupScheduleForm(forms.ModelForm):
    class Meta:
        model = PickupSchedule
        fields = ['title', 'zone', 'collector', 'scheduled_date', 'scheduled_time',
                  'frequency', 'estimated_kg', 'notes']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. GRA Phase 2 Monday Pickup'}),
            'zone': forms.Select(attrs={'class': 'form-select'}),
            'collector': forms.Select(attrs={'class': 'form-select'}),
            'scheduled_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'scheduled_time': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'frequency': forms.Select(attrs={'class': 'form-select'}),
            'estimated_kg': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '0.00'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Additional notes...'}),
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['resident_name', 'resident_phone', 'resident_email', 'address',
                  'zone', 'appointment_type', 'appointment_date', 'appointment_time', 'description']
        widgets = {
            'resident_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full name'}),
            'resident_phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+234 ...'}),
            'resident_email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'email@example.com'}),
            'address': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2, 'placeholder': 'Street address, area, LGA'}),
            'zone': forms.Select(attrs={'class': 'form-select'}),
            'appointment_type': forms.Select(attrs={'class': 'form-select'}),
            'appointment_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Describe the issue or request...'}),
        }


class ScheduleStatusForm(forms.ModelForm):
    class Meta:
        model = PickupSchedule
        fields = ['status', 'actual_kg', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'actual_kg': forms.NumberInput(attrs={'class': 'form-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }


class AppointmentStatusForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['status', 'assigned_collector']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'assigned_collector': forms.Select(attrs={'class': 'form-select'}),
        }

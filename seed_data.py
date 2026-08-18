import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cleancity.settings')

import django
django.setup()

from scheduling.models import Zone, WasteCollector, PickupSchedule, Appointment
from datetime import date, time, timedelta

print("Seeding CleanCity database...")

# Zones
zones_data = [
    ("GRA Zone", "Government Reserved Area (Phase 1 & 2)", "#3aff6c"),
    ("D/Line Zone", "Diobu, Mile 1 & 2", "#4da6ff"),
    ("Rumuola Zone", "Rumuola, Rumuobiakani", "#f5e642"),
    ("Eliozu Zone", "Eliozu, Woji, Rumuepirikom", "#ff7a35"),
    ("Trans-Amadi Zone", "Trans-Amadi Industrial Layout", "#c084fc"),
]
zones = {}
for name, area, color in zones_data:
    z, _ = Zone.objects.get_or_create(name=name, defaults={'area': area, 'color': color})
    zones[name] = z
    print(f"  Zone: {name}")

# Collectors
collectors_data = [
    ("Chukwuemeka Obi", "08031234567", "PHC-001-TRK", "truck", "GRA Zone"),
    ("Amara Nwosu", "08047654321", "PHC-002-TRK", "truck", "D/Line Zone"),
    ("Tunde Adeyemi", "08059876543", "PHC-003-TRI", "tricycle", "Rumuola Zone"),
    ("Blessing Eze", "08061112233", "PHC-004-VAN", "van", "Eliozu Zone"),
    ("Ifeanyi Okwu", "08074445566", "PHC-005-TRK", "truck", "Trans-Amadi Zone"),
]
collectors = []
for name, phone, vno, vtype, zone_name in collectors_data:
    c, _ = WasteCollector.objects.get_or_create(name=name, defaults={
        'phone': phone, 'vehicle_number': vno, 'vehicle_type': vtype, 'zone': zones[zone_name]
    })
    collectors.append((c, zones[zone_name]))
    print(f"  Collector: {name}")

# Schedules
today = date.today()
schedule_titles = [
    ("GRA Monday Morning Pickup", "weekly"),
    ("D/Line Tuesday Sweep", "weekly"),
    ("Rumuola Wednesday Collection", "weekly"),
    ("Eliozu Thursday Pickup", "biweekly"),
    ("Trans-Amadi Friday Industrial", "weekly"),
    ("GRA Saturday Bulk Run", "once"),
]
times = [time(7, 0), time(8, 30), time(9, 0), time(7, 30), time(8, 0), time(10, 0)]
statuses = ['completed', 'completed', 'in_progress', 'scheduled', 'scheduled', 'scheduled']

for i, ((title, freq), t, status) in enumerate(zip(schedule_titles, times, statuses)):
    collector, zone = collectors[i % len(collectors)]
    sched_date = today - timedelta(days=2) if status == 'completed' else today + timedelta(days=i)
    s, _ = PickupSchedule.objects.get_or_create(title=title, defaults={
        'zone': zone,
        'collector': collector,
        'scheduled_date': sched_date,
        'scheduled_time': t,
        'frequency': freq,
        'status': status,
        'estimated_kg': 500 + i * 75,
        'actual_kg': 480 + i * 60 if status == 'completed' else None,
    })
    print(f"  Schedule: {title}")

# Appointments
appts = [
    ("Chioma Okafor", "08091234567", "chioma@email.com",
     "12 Aba Road, GRA Phase 2", "GRA Zone", "bulk", today + timedelta(days=1), time(9, 0), "pending"),
    ("Mr. James Peterside", "08042345678", "",
     "45 Rumuola Road", "Rumuola Zone", "hazardous", today + timedelta(days=2), time(11, 0), "confirmed"),
    ("Ngozi Dike", "08053456789", "ngozi@corp.ng",
     "Trans-Amadi Industrial, Block C", "Trans-Amadi Zone", "recycling", today + timedelta(days=3), time(8, 30), "pending"),
]
for name, phone, email, addr, zone_name, atype, adate, atime, status in appts:
    Appointment.objects.get_or_create(resident_phone=phone, appointment_date=adate, defaults={
        'resident_name': name,
        'resident_email': email,
        'address': addr,
        'zone': zones[zone_name],
        'appointment_type': atype,
        'appointment_time': atime,
        'status': status,
    })
    print(f"  Appointment: {name}")

print("\n✅ Database seeded successfully!")
print("Run: python manage.py runserver")

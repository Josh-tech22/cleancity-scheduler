# CleanCity PHC — Scheduling System
> Waste management scheduling platform for Port Harcourt, Nigeria

## Quick Setup (5 minutes)

### 1. Install Django
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Create Admin User
```bash
python manage.py createsuperuser
```
Enter a username, email, and password when prompted.

### 4. Seed Sample Data
```bash
python seed_data.py
```
This populates 5 zones, 5 collectors, 6 schedules, and 3 appointments.

### 5. Start the Server
```bash
python manage.py runserver
```

### 6. Open in Browser
- **App:** http://127.0.0.1:8000/
- **Admin:** http://127.0.0.1:8000/admin/

---

## Pages & Features

| Page | URL | Description |
|------|-----|-------------|
| Dashboard | / | Stats, charts, recent activity |
| Schedules | /schedules/ | List, filter, create pickup schedules |
| Appointments | /appointments/ | Resident appointment bookings |
| Collectors | /collectors/ | Waste collector profiles |
| Zones | /zones/ | Collection zone management |
| Admin | /admin/ | Full data management |

## Adding Data via Admin Panel
1. Go to http://127.0.0.1:8000/admin/
2. Log in with your superuser credentials
3. Add **Zones** first, then **Collectors**, then **Schedules**

## Project Structure
```
cleancity_scheduler/
├── manage.py
├── requirements.txt
├── seed_data.py          ← Run once to load sample data
├── cleancity/            ← Django project config
│   ├── settings.py
│   └── urls.py
└── scheduling/           ← Main app
    ├── models.py         ← Zone, Collector, Schedule, Appointment
    ├── views.py          ← All page logic
    ├── forms.py          ← Form definitions
    ├── urls.py           ← URL routing
    ├── admin.py          ← Admin panel config
    └── templates/        ← HTML templates
```

## Tech Stack
- **Backend:** Python 3.10+ / Django 4.2
- **Database:** SQLite (swap to PostgreSQL for production)
- **Frontend:** Pure HTML/CSS/JS (no additional dependencies)
- **Timezone:** Africa/Lagos (WAT)

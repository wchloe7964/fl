# Flight Booking System

A complete flight booking system built with Django and SQLite, designed for deployment on PythonAnywhere.

## Features

- Flight search and booking
- User authentication
- Payment processing
- Admin dashboard
- REST API
- Responsive design

## Quick Start

### Local Development

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate venv: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Configure environment: `cp .env.example .env`
6. Run migrations: `python manage.py migrate`
7. Create superuser: `python manage.py createsuperuser`
8. Populate data: `python manage.py populate_sample_data`
9. Run server: `python manage.py runserver`

### PythonAnywhere Deployment

1. Upload files to your PythonAnywhere account
2. Run setup script: `bash setup_pythonanywhere.sh`
3. Run deployment: `bash deploy.sh`
4. Configure web app in PythonAnywhere dashboard
5. Set static files paths in web app configuration

## API Endpoints

- `GET /api/flights/` - List all flights
- `GET /api/flights/search/` - Search flights
- `GET /api/airports/` - List airports
- `POST /api/bookings/` - Create booking
- `POST /api/payments/process/` - Process payment

## Admin Access

Access the admin panel at `/admin/` with your superuser credentials.

## Backup Strategy

Automated daily backups are configured. Manual backup: `python manage.py backup_database`

## Security Features

- CSRF protection
- Secure cookies
- SQL injection prevention
- XSS protection
- Clickjacking protection
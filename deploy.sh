#!/bin/bash

# Flight Booking System Deployment Script for PythonAnywhere

echo "Starting deployment process..."

# Activate virtual environment
source ~/.virtualenvs/flight-booking-env/bin/activate

# Navigate to project directory
cd ~/flight-booking-system

# Pull latest changes (if using git)
# git pull origin main

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if not exists (uncomment if needed)
# echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'password')" | python manage.py shell

# Populate sample data
echo "Populating sample data..."
python manage.py populate_sample_data

# Backup database
echo "Backing up database..."
python manage.py backup_database

echo "Deployment completed successfully!"
echo "Please reload your web app in the PythonAnywhere dashboard."
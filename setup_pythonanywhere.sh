#!/bin/bash

# PythonAnywhere Setup Script

echo "Setting up Flight Booking System on PythonAnywhere..."

# Create virtual environment
mkvirtualenv flight-booking-env --python=python3.9

# Activate virtual environment
workon flight-booking-env

# Install Django and dependencies
pip install django==4.2.7

# Create project directory (if not exists)
mkdir -p ~/flight-booking-system
cd ~/flight-booking-system

echo "Setup completed. Please upload your project files to ~/flight-booking-system/"
echo "Then run: ./deploy.sh"
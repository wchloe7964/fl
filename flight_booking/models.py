from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
import random
import string

class Airport(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100, db_index=True)
    city = models.CharField(max_length=100, db_index=True)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['city', 'country']),
        ]
        ordering = ['city']
    
    def __str__(self):
        return f"{self.code} - {self.city}"

class Flight(models.Model):
    FLIGHT_TYPES = [
        ('domestic', 'Domestic'),
        ('international', 'International'),
    ]
    
    flight_number = models.CharField(max_length=10, db_index=True)
    airline = models.CharField(max_length=100)
    departure_airport = models.ForeignKey(Airport, related_name='departures', on_delete=models.CASCADE)
    arrival_airport = models.ForeignKey(Airport, related_name='arrivals', on_delete=models.CASCADE)
    departure_time = models.DateTimeField(db_index=True)
    arrival_time = models.DateTimeField()
    duration = models.DurationField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    total_seats = models.IntegerField(default=180)
    available_seats = models.IntegerField(default=180)
    flight_type = models.CharField(max_length=20, choices=FLIGHT_TYPES, default='domestic')
    
    class Meta:
        indexes = [
            models.Index(fields=['departure_airport', 'arrival_airport', 'departure_time']),
        ]
        ordering = ['departure_time']
    
    def __str__(self):
        return f"{self.airline} {self.flight_number}"
    
    def save(self, *args, **kwargs):
        # Calculate duration if not set
        if self.departure_time and self.arrival_time and not self.duration:
            self.duration = self.arrival_time - self.departure_time
        super().save(*args, **kwargs)

class Booking(models.Model):
    BOOKING_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    booking_reference = models.CharField(max_length=8, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending')
    seats_booked = models.IntegerField(default=1)
    
    class Meta:
        ordering = ['-booking_date']
    
    def save(self, *args, **kwargs):
        if not self.booking_reference:
            self.booking_reference = self.generate_booking_reference()
        if not self.total_price:
            self.total_price = self.flight.price * self.seats_booked
        super().save(*args, **kwargs)
    
    def generate_booking_reference(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    def __str__(self):
        return f"Booking {self.booking_reference}"

class Passenger(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    booking = models.ForeignKey(Booking, related_name='passengers', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    passport_number = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Payment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
    ]
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"Payment for {self.booking.booking_reference}"
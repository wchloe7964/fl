from django.contrib import admin
from .models import Airport, Flight, Booking, Passenger, Payment

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'city', 'country']
    search_fields = ['code', 'name', 'city']
    list_filter = ['country']

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ['flight_number', 'airline', 'departure_airport', 'arrival_airport', 
                   'departure_time', 'price', 'available_seats', 'flight_type']
    list_filter = ['airline', 'flight_type', 'departure_time']
    search_fields = ['flight_number', 'airline']
    readonly_fields = ['duration']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_reference', 'user', 'flight', 'booking_date', 'total_price', 'status']
    list_filter = ['status', 'booking_date']
    search_fields = ['booking_reference', 'user__username']
    readonly_fields = ['booking_reference', 'booking_date']

@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'booking', 'date_of_birth']
    search_fields = ['first_name', 'last_name']
    list_filter = ['gender']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['booking', 'amount', 'payment_method', 'status', 'payment_date']
    list_filter = ['status', 'payment_method']
    readonly_fields = ['payment_date']
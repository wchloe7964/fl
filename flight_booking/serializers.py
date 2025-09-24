from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Airport, Flight, Booking, Passenger, Payment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'

class FlightSerializer(serializers.ModelSerializer):
    departure_airport = AirportSerializer(read_only=True)
    arrival_airport = AirportSerializer(read_only=True)
    departure_airport_id = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(), source='departure_airport', write_only=True
    )
    arrival_airport_id = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(), source='arrival_airport', write_only=True
    )
    
    class Meta:
        model = Flight
        fields = '__all__'

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    flight = FlightSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    passengers = PassengerSerializer(many=True, read_only=True)
    flight_id = serializers.PrimaryKeyRelatedField(
        queryset=Flight.objects.all(), source='flight', write_only=True
    )
    
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['booking_reference', 'user', 'booking_date', 'total_price']

class PaymentSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'
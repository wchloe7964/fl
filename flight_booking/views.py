from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Airport, Flight, Booking, Passenger, Payment
from .serializers import *

class AirportViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if query:
            airports = Airport.objects.filter(
                Q(city__icontains=query) | 
                Q(name__icontains=query) |
                Q(code__icontains=query)
            )[:10]
            serializer = self.get_serializer(airports, many=True)
            return Response(serializer.data)
        return Response([])

class FlightViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        departure = request.query_params.get('departure')
        arrival = request.query_params.get('arrival')
        date = request.query_params.get('date')
        passengers = int(request.query_params.get('passengers', 1))
        
        if not all([departure, arrival, date]):
            return Response(
                {'error': 'Departure, arrival, and date are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            search_date = datetime.strptime(date, '%Y-%m-%d').date()
            next_day = search_date + timedelta(days=1)
            
            flights = Flight.objects.filter(
                Q(departure_airport__city__icontains=departure) |
                Q(departure_airport__code__icontains=departure),
                Q(arrival_airport__city__icontains=arrival) |
                Q(arrival_airport__code__icontains=arrival),
                departure_time__date=search_date,
                available_seats__gte=passengers
            ).select_related('departure_airport', 'arrival_airport')
            
            serializer = self.get_serializer(flights, many=True)
            return Response(serializer.data)
        
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def book(self, request, pk=None):
        flight = self.get_object()
        seats = int(request.data.get('seats', 1))
        
        if flight.available_seats < seats:
            return Response(
                {'error': 'Not enough seats available'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # In a real implementation, you'd create a booking here
        return Response({
            'message': 'Flight booking initiated',
            'flight': flight.flight_number,
            'seats': seats,
            'total_price': float(flight.price) * seats
        })

class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        flight = serializer.validated_data['flight']
        seats_booked = serializer.validated_data.get('seats_booked', 1)
        
        if flight.available_seats < seats_booked:
            raise serializers.ValidationError("Not enough seats available")
        
        # Update available seats
        flight.available_seats -= seats_booked
        flight.save()
        
        total_price = flight.price * seats_booked
        booking = serializer.save(user=self.request.user, total_price=total_price)
        
        # Create payment record
        Payment.objects.create(
            booking=booking,
            amount=total_price,
            payment_method=serializer.validated_data.get('payment_method', 'credit_card')
        )

class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    
    def get_queryset(self):
        return Payment.objects.filter(booking__user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        payment = self.get_object()
        
        # Simulate payment processing
        payment.status = 'success'
        payment.transaction_id = f"TXN{timezone.now().strftime('%Y%m%d%H%M%S')}"
        payment.save()
        
        # Update booking status
        payment.booking.status = 'confirmed'
        payment.booking.save()
        
        return Response({
            'status': 'success', 
            'transaction_id': payment.transaction_id,
            'message': 'Payment processed successfully'
        })
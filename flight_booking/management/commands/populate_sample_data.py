from django.core.management.base import BaseCommand
from flight_booking.models import Airport, Flight
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populate database with sample flight data'
    
    def handle(self, *args, **options):
        self.stdout.write('Populating sample data...')
        
        # Create airports
        airports_data = [
            {'code': 'JFK', 'name': 'John F. Kennedy International Airport', 'city': 'New York', 'country': 'USA'},
            {'code': 'LAX', 'name': 'Los Angeles International Airport', 'city': 'Los Angeles', 'country': 'USA'},
            {'code': 'ORD', 'name': 'O\'Hare International Airport', 'city': 'Chicago', 'country': 'USA'},
            {'code': 'LHR', 'name': 'Heathrow Airport', 'city': 'London', 'country': 'UK'},
            {'code': 'CDG', 'name': 'Charles de Gaulle Airport', 'city': 'Paris', 'country': 'France'},
            {'code': 'DXB', 'name': 'Dubai International Airport', 'city': 'Dubai', 'country': 'UAE'},
            {'code': 'SIN', 'name': 'Changi Airport', 'city': 'Singapore', 'country': 'Singapore'},
            {'code': 'BKK', 'name': 'Suvarnabhumi Airport', 'city': 'Bangkok', 'country': 'Thailand'},
        ]
        
        airports = {}
        for airport_data in airports_data:
            airport, created = Airport.objects.get_or_create(
                code=airport_data['code'],
                defaults=airport_data
            )
            airports[airport.code] = airport
            self.stdout.write(f'{"Created" if created else "Found"} airport: {airport}')
        
        # Create sample flights
        airlines = ['American Airlines', 'Delta Air Lines', 'United Airlines', 'Emirates', 'Singapore Airlines']
        base_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        flight_routes = [
            ('JFK', 'LAX', 6, 299.99),
            ('JFK', 'LHR', 7, 599.99),
            ('LAX', 'DXB', 15, 899.99),
            ('ORD', 'CDG', 8, 699.99),
            ('LHR', 'SIN', 13, 799.99),
            ('CDG', 'BKK', 11, 749.99),
            ('JFK', 'ORD', 2, 199.99),
            ('LAX', 'ORD', 4, 349.99),
        ]
        
        for i, (dep_code, arr_code, duration_hours, price) in enumerate(flight_routes):
            for day_offset in range(0, 30, 2):  # Flights every 2 days for next 30 days
                departure_time = base_time + timedelta(days=day_offset, hours=random.randint(6, 22))
                arrival_time = departure_time + timedelta(hours=duration_hours)
                
                flight_number = f"{dep_code}{arr_code}{day_offset:02d}"
                
                flight, created = Flight.objects.get_or_create(
                    flight_number=flight_number,
                    defaults={
                        'airline': random.choice(airlines),
                        'departure_airport': airports[dep_code],
                        'arrival_airport': airports[arr_code],
                        'departure_time': departure_time,
                        'arrival_time': arrival_time,
                        'duration': timedelta(hours=duration_hours),
                        'price': price,
                        'total_seats': 180,
                        'available_seats': random.randint(50, 180),
                        'flight_type': 'international' if dep_code != arr_code and dep_code[-2:] != arr_code[-2:] else 'domestic'
                    }
                )
                
                if created:
                    self.stdout.write(f'Created flight: {flight}')
        
        self.stdout.write(self.style.SUCCESS('Successfully populated sample data!'))
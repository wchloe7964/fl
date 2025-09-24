// Flight Booking System Main JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Flight Search Functionality
    const flightSearchForm = document.getElementById('flightSearchForm');
    if (flightSearchForm) {
        flightSearchForm.addEventListener('submit', handleFlightSearch);
    }

    // Initialize date picker with tomorrow's date
    const dateInput = document.getElementById('date');
    if (dateInput) {
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        dateInput.value = tomorrow.toISOString().split('T')[0];
        dateInput.min = tomorrow.toISOString().split('T')[0];
    }

    // Load sample flights on page load
    if (window.location.pathname === '/flights/') {
        loadSampleFlights();
    }
});

async function handleFlightSearch(e) {
    e.preventDefault();
    
    const departure = document.getElementById('departure').value;
    const arrival = document.getElementById('arrival').value;
    const date = document.getElementById('date').value;
    const passengers = document.getElementById('passengers').value;

    if (!departure || !arrival || !date) {
        showAlert('Please fill in all fields', 'danger');
        return;
    }

    try {
        const response = await fetch(`/api/flights/search/?departure=${encodeURIComponent(departure)}&arrival=${encodeURIComponent(arrival)}&date=${date}&passengers=${passengers}`);
        const flights = await response.json();
        
        displayFlightResults(flights);
    } catch (error) {
        console.error('Error searching flights:', error);
        showAlert('Error searching for flights. Please try again.', 'danger');
    }
}

function displayFlightResults(flights) {
    const resultsContainer = document.getElementById('flightResults');
    
    if (!flights || flights.length === 0) {
        resultsContainer.innerHTML = `
            <div class="text-center py-4">
                <i class="fas fa-plane-slash fa-3x text-muted mb-3"></i>
                <p class="text-muted">No flights found matching your criteria.</p>
                <button class="btn btn-outline-primary" onclick="loadSampleFlights()">View Sample Flights</button>
            </div>
        `;
        return;
    }

    resultsContainer.innerHTML = flights.map(flight => `
        <div class="flight-card card mb-3">
            <div class="card-body">
                <div class="row align-items-center">
                    <div class="col-md-3">
                        <h6 class="mb-1">${flight.departure_airport.city} → ${flight.arrival_airport.city}</h6>
                        <small class="text-muted">${flight.airline} • ${flight.flight_number}</small>
                    </div>
                    <div class="col-md-2">
                        <strong>${new Date(flight.departure_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</strong>
                        <br>
                        <small>${flight.departure_airport.code}</small>
                    </div>
                    <div class="col-md-2 text-center">
                        <small class="text-muted">${formatDuration(flight.duration)}</small>
                        <div class="flight-line"></div>
                    </div>
                    <div class="col-md-2">
                        <strong>${new Date(flight.arrival_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</strong>
                        <br>
                        <small>${flight.arrival_airport.code}</small>
                    </div>
                    <div class="col-md-2 text-center">
                        <h5 class="text-primary mb-1">$${flight.price}</h5>
                        <small class="text-muted">${flight.available_seats} seats left</small>
                    </div>
                    <div class="col-md-1">
                        <button class="btn btn-primary btn-sm" onclick="bookFlight(${flight.id})">
                            Book Now
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

function formatDuration(duration) {
    const hours = Math.floor(duration / 3600);
    const minutes = Math.floor((duration % 3600) / 60);
    return `${hours}h ${minutes}m`;
}

async function loadSampleFlights() {
    try {
        const response = await fetch('/api/flights/');
        const flights = await response.json();
        displayFlightResults(flights.results || flights);
    } catch (error) {
        console.error('Error loading flights:', error);
        // Fallback to static sample data
        displaySampleFlights();
    }
}

function displaySampleFlights() {
    const resultsContainer = document.getElementById('flightResults');
    resultsContainer.innerHTML = `
        <div class="alert alert-info">
            <i class="fas fa-info-circle"></i> Showing sample flights. Search for specific routes to see real results.
        </div>
        ${getSampleFlights().map(flight => `
            <div class="flight-card card mb-3">
                <div class="card-body">
                    <div class="row align-items-center">
                        <div class="col-md-3">
                            <h6 class="mb-1">${flight.route}</h6>
                            <small class="text-muted">${flight.airline} • ${flight.number}</small>
                        </div>
                        <div class="col-md-2">
                            <strong>${flight.departure}</strong>
                            <br>
                            <small>${flight.fromCode}</small>
                        </div>
                        <div class="col-md-2 text-center">
                            <small class="text-muted">${flight.duration}</small>
                            <div class="flight-line"></div>
                        </div>
                        <div class="col-md-2">
                            <strong>${flight.arrival}</strong>
                            <br>
                            <small>${flight.toCode}</small>
                        </div>
                        <div class="col-md-2 text-center">
                            <h5 class="text-primary mb-1">$${flight.price}</h5>
                            <small class="text-muted">${flight.seats} seats left</small>
                        </div>
                        <div class="col-md-1">
                            <button class="btn btn-primary btn-sm" onclick="showBookingAlert()">
                                Book Now
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `).join('')}
    `;
}

function getSampleFlights() {
    return [
        {
            route: "New York → Los Angeles",
            airline: "American Airlines",
            number: "AA123",
            departure: "08:00 AM",
            fromCode: "JFK",
            duration: "6h 0m",
            arrival: "11:00 AM",
            toCode: "LAX",
            price: "299.99",
            seats: "45"
        },
        {
            route: "New York → London",
            airline: "British Airways",
            number: "BA456",
            departure: "06:30 PM",
            fromCode: "JFK",
            duration: "7h 30m",
            arrival: "06:00 AM",
            toCode: "LHR",
            price: "599.99",
            seats: "12"
        },
        {
            route: "Los Angeles → Dubai",
            airline: "Emirates",
            number: "EK789",
            departure: "10:15 PM",
            fromCode: "LAX",
            duration: "15h 45m",
            arrival: "02:00 AM",
            toCode: "DXB",
            price: "899.99",
            seats: "28"
        }
    ];
}

function bookFlight(flightId) {
    if (!isUserAuthenticated()) {
        showAlert('Please log in to book flights.', 'warning');
        window.location.href = '/admin/login/?next=/flights/';
        return;
    }
    
    window.location.href = `/booking/?flight=${flightId}`;
}

function isUserAuthenticated() {
    // Simple check - in real implementation, use proper authentication
    return document.cookie.includes('sessionid');
}

function showBookingAlert() {
    showAlert('Please log in to book flights.', 'info');
}

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('main .container');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Airport autocomplete functionality
function setupAirportAutocomplete() {
    const departureInput = document.getElementById('departure');
    const arrivalInput = document.getElementById('arrival');
    
    if (departureInput) {
        departureInput.addEventListener('input', debounce(handleAirportSearch, 300));
    }
    if (arrivalInput) {
        arrivalInput.addEventListener('input', debounce(handleAirportSearch, 300));
    }
}

async function handleAirportSearch(e) {
    const query = e.target.value;
    if (query.length < 2) return;
    
    try {
        const response = await fetch(`/api/airports/search/?q=${encodeURIComponent(query)}`);
        const airports = await response.json();
        
        showAirportSuggestions(e.target, airports);
    } catch (error) {
        console.error('Error searching airports:', error);
    }
}

function showAirportSuggestions(input, airports) {
    // Remove existing suggestions
    const existingList = input.parentNode.querySelector('.suggestions-list');
    if (existingList) {
        existingList.remove();
    }
    
    if (airports.length === 0) return;
    
    const suggestionsList = document.createElement('ul');
    suggestionsList.className = 'suggestions-list list-group';
    suggestionsList.style.position = 'absolute';
    suggestionsList.style.zIndex = '1000';
    suggestionsList.style.width = '100%';
    
    airports.forEach(airport => {
        const listItem = document.createElement('li');
        listItem.className = 'list-group-item list-group-item-action';
        listItem.textContent = `${airport.city} (${airport.code}) - ${airport.name}`;
        listItem.style.cursor = 'pointer';
        
        listItem.addEventListener('click', () => {
            input.value = airport.city;
            suggestionsList.remove();
        });
        
        suggestionsList.appendChild(listItem);
    });
    
    input.parentNode.style.position = 'relative';
    input.parentNode.appendChild(suggestionsList);
    
    // Remove suggestions when clicking outside
    document.addEventListener('click', function removeSuggestions(e) {
        if (!input.parentNode.contains(e.target)) {
            suggestionsList.remove();
            document.removeEventListener('click', removeSuggestions);
        }
    });
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialize when page loads
setupAirportAutocomplete();
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'airports', views.AirportViewSet)
router.register(r'flights', views.FlightViewSet)
router.register(r'bookings', views.BookingViewSet)
router.register(r'payments', views.PaymentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('flights/', TemplateView.as_view(template_name='flights.html'), name='flights'),
    path('booking/', TemplateView.as_view(template_name='booking.html'), name='booking'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
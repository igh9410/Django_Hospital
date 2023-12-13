"""
URL configuration for django_hospital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from appointments.views import AppointmentViewSet

from doctors.views import DoctorViewSet

urlpatterns =[  
    path('admin/', admin.site.urls),
    path('api/doctors/', include([
        path('search-by-string/', DoctorViewSet.as_view({'get': 'search_doctors_by_string'}), name='doctor-search-by-string'),
        path('search-by-datetime/', DoctorViewSet.as_view({'get': 'search_doctors_by_datetime'}), name='doctor-search-by-datetime'),
    ])),
    path('api/appointments/', AppointmentViewSet.as_view({'post': 'create'}), name='appointment-request-create')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

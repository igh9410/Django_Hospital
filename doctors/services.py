import datetime
import logging
from doctors.models import Doctor
from django.db.models import Q

def search_doctors_by_string(query):
    if not query:
        return None
    
    return Doctor.objects.filter(
        Q(name__icontains=query) | # Search by doctor name
        Q(specialties__name__icontains=query) | # Search by specialty
        Q(hospital__icontains=query) # Search by hospital 
    ).distinct()

def search_doctors_by_datetime(query_datetime_str):
    # Parse the datetime string into a datetime object
    try:
        query_datetime = datetime.datetime.strptime(query_datetime_str, "%Y-%m-%d %H:%M")
    except ValueError:
        logging.info("Invalid datetime format")
        return Doctor.objects.none()

    day_of_week = query_datetime.strftime("%A")
    query_time = query_datetime.time()

    # Query doctors who are working on the given day and time
    working_doctors = Doctor.objects.filter(
        working_hours__day_of_week=day_of_week,
        working_hours__start_time__lte=query_time,
        working_hours__end_time__gte=query_time
    ).distinct()

    return working_doctors
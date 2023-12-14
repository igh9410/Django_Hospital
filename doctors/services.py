from datetime import date, datetime
import logging
from doctors.models import Doctor
from django.db.models import Q

def search_doctors_by_string(query):
    if not query:
        return None
    query_terms = query.split()  # Split the query string into words

    combined_query = Q()

    for term in query_terms:
        # Build a query for the current term
        term_query = Q(name__icontains=term) | Q(specialties__name__icontains=term) | Q(hospital__icontains=term) | Q(non_reimbursements__name__icontains=term)
        combined_query &= term_query  # Combine with the main query using logical AND
    
    return Doctor.objects.filter(combined_query).distinct()


def search_doctors_by_datetime(query_datetime_str):
    weekday_mapping = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday',
    }
     
    # Parse the datetime string into a datetime object
    try:
        query_datetime = datetime.strptime(query_datetime_str, "%Y-%m-%d %H:%M")
        day_of_week_num = query_datetime.weekday()     
    except ValueError:
        logging.info("Invalid datetime format")
        return Doctor.objects.none()
    
   

    day_of_week = weekday_mapping[day_of_week_num] # Map day of week from integer to string, for example 0 -> 'Monday', 1 -> 'Tuesday'...
    query_time = query_datetime.time()

    # Query doctors who are working on the given day and time
    working_doctors = Doctor.objects.filter(
        working_hours__day_of_week=day_of_week,
        working_hours__start_time__lte=query_time,
        working_hours__end_time__gte=query_time
    ).distinct()

    return working_doctors
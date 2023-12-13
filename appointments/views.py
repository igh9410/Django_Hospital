from django.utils import timezone
import pytz
from rest_framework import viewsets, status
from rest_framework.response import Response
from appointments.serializers import AppointmentRequestSerializer
from appointments.services import create_appointment_request_service
from .models import AppointmentRequest
# Create your views here.


class AppointmentViewSet(viewsets.ViewSet):
    queryset = AppointmentRequest.objects.all()

    def create(self, request):
        serializer = AppointmentRequestSerializer(data=request.data)
        print("Request Data:", request.data)  # Debugging statement
        print()
        

        if serializer.is_valid():
            print("serializer_validated_data:", serializer.validated_data)
            patient = serializer.validated_data['patient']  # Access the patient object
            doctor = serializer.validated_data['doctor']  # Access the doctor object
            preferred_datetime = serializer.validated_data['preferred_datetime']
            
            unconverted_datetime = timezone.now()
            seoul_timezone = pytz.timezone('Asia/Seoul')
            request_datetime = unconverted_datetime.astimezone(seoul_timezone) # The time when the API endpoint is called
            print("request_datetime in view: ", request_datetime)
            
            result = create_appointment_request_service(patient.id, doctor.id, preferred_datetime, request_datetime)
            
   
            if "error" not in result:
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


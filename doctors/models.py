import uuid
from django.db import models
# Create your models here.

class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, db_index=True)
    hospital = models.CharField(max_length=100, db_index=True, default="")
    specialties = models.ManyToManyField(Specialty)

    def __str__(self):
        return self.name

class WorkingHour(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    
    class Meta:
        unique_together = ('doctor', 'day_of_week')


    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='working_hours')
    day_of_week = models.CharField(max_length=9, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    break_start_time = models.TimeField(null=True, blank=True) # break time can be omitted 
    break_end_time = models.TimeField(null=True, blank=True) # break time can be omitted
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.doctor.name} - {self.day_of_week} {self.start_time} to {self.end_time} break time: {self.break_start_time} to {self.break_end_time}"





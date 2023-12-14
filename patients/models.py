import uuid
from django.db import models

# Create your models here.
class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name
    

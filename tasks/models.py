from django.db import models

# Create your models here.

class Task(models.Model):

    description = models.CharField(max_length=100)
    is_completed = models.BooleanField()
    created_at = models.DateField(null=True, blank=True)


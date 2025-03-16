from django.db import models

# Create your models here.

class Task(models.Model):

    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(null=True, blank=True)


class CompletedTask(models.Model):
    description = models.CharField(max_length=100)
    created_at = models.DateField(null=True, blank=True)
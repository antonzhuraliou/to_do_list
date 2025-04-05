from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=2)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(null=True, blank=True)


class CompletedTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=2)
    description = models.CharField(max_length=100)
    created_at = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=True)
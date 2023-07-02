from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.



class CustomUser(AbstractUser):
    is_manager = models.BooleanField(default=False)
    is_developer = models.BooleanField(default=False)


class Task(models.Model):
    STATUS_CHOICES = (
        ('todo', 'Todo'),
        ('in_progress', 'In Progress'),
        ('done', 'Done')
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


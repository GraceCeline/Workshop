import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Tool(models.Model):
    tool = models.CharField(max_length=300)

    def __str__(self):
        return self.tool
        
class Workshop(models.Model):
    
    workshop_title = models.CharField(max_length=500, unique=True)
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    further_info_link = models.URLField(blank=True, null=True)
    tool = models.ManyToManyField(Tool,blank=True)
    prerequisite = models.TextField(blank=True)
    PRESENCE = [
        ('onsite', 'Onsite'),
        ('hybrid', 'Hybrid'),
        ('online', 'Online'),
    ]
    type_of_presence = models.CharField(max_length=10, choices=PRESENCE)
    location = models.CharField(max_length=250)
    host = models.CharField(max_length=300, null=True)
    registration_link = models.URLField(blank=True, null=True)
    registration_deadline = models.DateField()
    max_participants = models.IntegerField()
    is_private = models.BooleanField(default=True)
    workshop_admin = models.ForeignKey(User,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.workshop_title

    def past_workshop(self):
        return self.date < timezone.now().date()

    def deadline_overdue(self):
        return self.registration_deadline < timezone.now().date()

    """class Meta:
        permissions = [
            ('create_workshop', 'Create workshop'),
            ('edit_workshop', 'Edit workshop'),
            ('delete_workshop', 'Delete workshop'),
        ]
"""

# Create your models here.

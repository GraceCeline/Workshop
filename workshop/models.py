from django.db import models

class Workshop(models.Model):
    workshop_title = models.CharField(max_length=500, unique=True)
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    further_info_link = models.URLField(blank=True, null=True)
    tool = models.ManyToManyField('Tool',blank=True)
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
    max_participants = models.IntegerField()

    def __str__(self):
        return self.workshop_title

class Tool(models.Model):
    tool = models.CharField(max_length=300)

    def __str__(self):
        return self.tool

# Create your models here.

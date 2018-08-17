from django.db import models
from django.utils import timezone

class CarbonData(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    
    def publish(self):
        self.save()

    def __str__(self):
        return self.title
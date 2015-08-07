from django.db import models

# Create your models here.
class SegmentsConfig(models.Model):
    name = models.CharField(max_length=50, unique=True)
    rules_set = models.TextField()
    date_creation = models.DateField(auto_now_add=True)

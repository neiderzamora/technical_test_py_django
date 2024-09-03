from django.db import models

class Author(models.Model):
    
    COUNTRY_ORIGIN_CHOICES  = (
        ('CO', 'Colombia'),
        ('EC', 'Ecuador'),
        ('VE', 'Venezuela')
    )

    name = models.CharField(max_length=100)
    country_origin = models.CharField(max_length=100, choices=COUNTRY_ORIGIN_CHOICES, default='CO')
    date_death = models.DateField(null=True, blank=True)
    
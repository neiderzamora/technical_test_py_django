from django.db import models
from apps.authors.models import Author

class Book(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    authors = models.ManyToManyField(Author)
    page_number = models.PositiveIntegerField()
    editorial = models.CharField(max_length=255, blank=False, null=False)
    isbn = models.CharField(max_length=50, blank=False, null=False, unique=True)
from django.db import models
from apps.users.models import CustomUser
from apps.books.models import Book

class Loan(models.Model):
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('loaned', 'Loaned'),
        ('return', 'Return'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='disponible')
    loan_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
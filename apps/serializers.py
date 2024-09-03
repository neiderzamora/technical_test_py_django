from rest_framework import serializers
from apps.authors.models import Author
from apps.books.models import Book
from apps.service.models import Loan
from apps.users.models import CustomUser    

from .validators import *

class AuthorSerializer(serializers.ModelSerializer):
    date_death = serializers.DateField(format='%Y-%m-%e')
    country_origin = serializers.CharField(validators=[validate_origin_country])
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        many=True,
        required=False
    )
    page_number = serializers.IntegerField(validators=[validate_page_number])
    class Meta:
        model = Book
        fields = '__all__'
    
    def validate_authors(self, data):
        """Validar que el libro tenga al menos un autor."""
        if 'authors' in data and len(data['authors']) == 0:
            raise serializers.ValidationError("El libro debe tener al menos un autor.")
        return data

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
        
    def validate(self, data):
        if data['status'] == 'borrowed':
            if Loan.objects.filter(book=data['book'], status='borrowed').exists():
                raise serializers.ValidationError("Este libro ya está prestado y no puede ser prestado nuevamente.")
        return data       
    
from django.core.exceptions import ValidationError
from rest_framework import serializers

def validate_origin_country(value):
    """Validar que el país de origen sea uno de los permitidos."""
    if value not in ['CO', 'EC', 'VE']:
        raise serializers.ValidationError("El país de origen debe ser Colombia (CO), Ecuador (EC), o Venezuela (VE).")
    return value

def validate_page_number(value):
    """Validar que el número de páginas no sea menor a 0."""
    if value <= 0:
        raise serializers.ValidationError("El número de páginas no puede ser menor a 0.")
    return value


from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import *

from apps.authors.models import Author
from apps.books.models import Book
from apps.users.models import CustomUser
from apps.service.models import Loan
from apps.users.models import CustomUser

from apps.serializers import *

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = []

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = []

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = []


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = []
    
    @action(detail=False, methods=['get'])
    def books_borrowed_by_user(self, request):
        user_id = request.query_params.get('user_id')
        
        if not user_id:
            return Response({"error": "El parámetro de consulta user_id es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        loans = Loan.objects.filter(user=user, status='loaned')
        book_isbns = [loan.book.isbn for loan in loans]
        
        return Response({"borrowed_books_isbns": book_isbns})
    
    @action(detail=True, methods=['post'])
    def loan(self, request, pk=None):
        loan = self.get_object()
        
        if loan.status != 'available':
            return Response({"error": "Este libro no está disponible para préstamo."}, status=status.HTTP_400_BAD_REQUEST)

        loan.status = 'loaned'
        loan.save()

        return Response({"message": "Libro prestado exitosamente.", "prestamo": PrestamoSerializer(loan).data})

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        loan = self.get_object()
        
        if loan.status != 'loaned':
            return Response({"error": "Este libro no está actualmente prestado."}, status=status.HTTP_400_BAD_REQUEST)
        
        loan.status = 'returned'
        loan.return_date = request.data.get('return_date')  
        loan.save()

        return Response({"message": "Libro devuelto exitosamente.", "prestamo": LoanSerializer(loan).data})

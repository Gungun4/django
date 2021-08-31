from django.shortcuts import render
from .models import Book


# Create your views here.
def all_book(request):
    all_book = Book.objects.all()

    return render(request, 'bookstore/all_book.html', locals())

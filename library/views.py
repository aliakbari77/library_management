from django.shortcuts import render
from django.views.generic import ListView

from library.models import Book

class BookListView(ListView):
    model = Book

    def get_queryset(self):
        queryset = Book.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        books = self.get_queryset()

        return render(request, "book_list.html", 
                      {'books': books})


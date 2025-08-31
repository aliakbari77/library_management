from django.shortcuts import render
from django.views.generic import ListView, CreateView, View
from django.shortcuts import redirect

from library.forms import BookForm
from library.models import Book

class BookListView(View):
    def get_queryset(self):
        queryset = Book.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        books = self.get_queryset()

        return render(request, "book_list.html", 
                      {'books': books})
    

class BookAddView(View):
    def get(self, request, *args, **kwargs):
        book_form = BookForm()
        return render(request, 'book_form.html', {'form': book_form})

    def post(self, request, *args, **kwargs):
        book_form = BookForm(request.POST, request.FILES)
        if book_form.is_valid():
            book_form.save()
            return redirect("book-list")
        else:
            return render(request, 'book_form.html', 
                          {'form': book_form})


class BookEditView(View):
    def get(self, request, book_id, *args, **kwargs):
        book = Book.objects.get(id=book_id)
        book_form = BookForm(instance=book)
        return render(request, 'book_form.html', {'book': book, 'form': book_form})

    def post(self, request, book_id, *args, **kwargs):
        book = Book.objects.get(id=book_id)
        book_form = BookForm(request.POST, request.FILES, instance=book)
        if book_form.is_valid():
            book_form.save()
            return redirect("book-list")
        else:
            return render(request, 'book_form.html', {'book': book, 'form': book_form})
        

class BookDetailView(View):
    def get(self, request, book_id, *args, **kwargs):
        book = Book.objects.get(id=book_id)
        return render(request, 'book_detail.html', {'book': book})
    

class BookDeleteView(View):
    def get(self, request, book_id, *args, **kwargs):
        book = Book.objects.get(id=book_id)
        book.delete()
        return redirect("book-list")    
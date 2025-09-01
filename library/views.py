from django.shortcuts import render
from django.views.generic import ListView, CreateView, View
from django.shortcuts import redirect

from library.filters import BookFilter
from library.forms import BookForm, CategoryForm
from library.models import Book


class BookListView(View):    
    def get_queryset(self):
        queryset = Book.objects.all()
        self.filterset = BookFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get(self, request, *args, **kwargs):
        books = self.get_queryset()

        return render(request, "book_list.html", 
                      {'books': books, 
                       'filterset': self.filterset})
    
    def post(self, request, *args, **kwargs):
        books = self.get_queryset()
        for book in books:
            book.delete()
        return redirect("book-list")
    

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


class CategoryAdd(View):
    def get(self, request, *args, **kwargs):
        category_form = CategoryForm()
        return render(request, 'category_form.html', {
            'form': category_form
        })
    
    def post(self, request, *args, **kwargs):
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            return redirect('book-list')
        
        return render(request, 'category_form.html', {
            'form': category_form
        })

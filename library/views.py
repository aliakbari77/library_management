from django.shortcuts import render
from django.views.generic import ListView, CreateView, View
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from library.filters import BookFilter
from library.forms import BookForm, CategoryForm, LoginForm, SignInForm
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


class CategoryAddView(View):
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


class SignInView(View):
    def get(self, request, *args, **kwargs):
        sign_in_form = SignInForm()
        return render(request, 'sign_in_form.html', {
            'form': sign_in_form
        })

    def post(self, request, *args, **kwargs):
        sign_in_form = SignInForm(request.POST)
        if sign_in_form.is_valid():
            sign_in_form.save()
            return redirect('book-list')
        return render(request, 'sign_in_form.html', {
            'form': sign_in_form
        })


class LoginView(View):
    def get(self, request, *args, **kwargs):
        login_form = LoginForm()
        return render(request, 'login_form.html', {
            'form': login_form
        })
    
    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('book-list')
        else:
            error_message = 'username or password is incorrect'
            return render(request, 'login_form.html', {
                'form': login_form,
                'error_message': error_message
            })


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('book-list')


class FavouriteBooksView(View):
    def get(self, request, *args, **kwargs):
        favourite_books = Book.objects.filter(favourites=request.user)
        return render(request, 'book_fav.html', {
            'books': favourite_books
        })
    

class ToggleFavouriteBookView(View):
    def post(self, request, book_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                "success": False,
                "message": "Unauthorized",
            }, status=401)
        
        book = Book.objects.get(id=book_id)

        if request.user in book.favourites.all():
            book.favourites.remove(request.user)
            is_favourite = False
        else:
            book.favourites.add(request.user)
            is_favourite = True

        return JsonResponse({
            "success": True,
            "is_favourite": is_favourite
        })
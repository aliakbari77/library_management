from django import forms
from library.models import Book, Category, Member
from django.contrib.auth.forms import AuthenticationForm

from django import forms
from .models import Book, Category, Author, Publisher

class BookForm(forms.ModelForm):
    published_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
            }
        ),
        input_formats=['%Y-%m-%d'],
        label="Published Date"
    )

    class Meta:
        model = Book
        fields = ['title', 'authors', 'category', 'publisher', 'published_date', 'picture']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Book Title'}),
            'authors': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
            'category': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
            'publisher': forms.Select(attrs={'class': 'form-select'}),
            'picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Book Title',
            'authors': 'Authors',
            'category': 'Categories',
            'publisher': 'Publisher',
            'picture': 'Book Cover',
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'}),
        }
        labels = {
            'name': 'Category Name',
        }

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None


class SignInForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )

    class Meta:
        model = Member
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
        help_texts = {
            'username': None,
        }

    def save(self, commit=True):
        user = Member.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        return user
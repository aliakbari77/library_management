from django import forms
from library.models import Book, Category, Member

class BookForm(forms.ModelForm):
    published_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',  
                'class': 'form-control', 
            }
        ),
        input_formats=['%Y-%m-%d'],  
    )
    class Meta:
        model = Book
        fields = ['title', 'authors', 'category', 'publisher', 'published_date', 'picture']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class LoginForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['username', 'password']
        help_texts = {
            'username': None,
        }
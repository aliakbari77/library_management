from django import forms
from library.models import Book, Category

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
        fields = ['title', 'authors', 'publisher', 'published_date', 'picture']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
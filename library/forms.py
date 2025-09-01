from django import forms
from library.models import Book, Category, Member
from django.contrib.auth.forms import AuthenticationForm

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


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None


class SignInForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['username', 'password', 'email']
        help_texts ={
            'username': None
        }

    def save(self, commit=True):
        new_member = self.instance
        Member.objects.create_user(
            username=new_member.username,
            email=new_member.email,
            password=new_member.password
        )
        return new_member
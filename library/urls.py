from django.urls import path
from library.views import BookAddView, BookListView

urlpatterns = [
    path('book/', BookListView.as_view(), name="book-list"),
    path('book/add/', BookAddView.as_view(), name='book-add')
]

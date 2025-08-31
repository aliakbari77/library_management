from django.urls import path
from library.views import BookAddView, BookEditView, BookListView

urlpatterns = [
    path('book/', BookListView.as_view(), name="book-list"),
    path('book/add/', BookAddView.as_view(), name='book-add'),
    path('book/edit/<int:book_id>/', BookEditView.as_view(), name='book-edit'),
]

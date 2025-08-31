from django.urls import path
from library.views import BookAddView, BookDetailView, BookEditView, BookListView

urlpatterns = [
    path('book/', BookListView.as_view(), name="book-list"),
    path('book/add/', BookAddView.as_view(), name='book-add'),
    path('book/edit/<int:book_id>/', BookEditView.as_view(), name='book-edit'),
    path('book/detail/<int:book_id>/', BookDetailView.as_view(), name='book-detail')
]

from django.urls import path
from library.views import BookAddView, BookDeleteView, BookDetailView, BookEditView, BookListView, CategoryAdd, FavouriteBooks

urlpatterns = [
    path('book/', BookListView.as_view(), name="book-list"),
    path('book/add/', BookAddView.as_view(), name='book-add'),
    path('book/edit/<int:book_id>/', BookEditView.as_view(), name='book-edit'),
    path('book/detail/<int:book_id>/', BookDetailView.as_view(), name='book-detail'),
    path('book/delete/<int:book_id>/', BookDeleteView.as_view(), name='book-delete'),
    path('book/category/add/', CategoryAdd.as_view(), name="category-add"),
    path('book/favourite/', FavouriteBooks.as_view(), name='book-favourite')
]

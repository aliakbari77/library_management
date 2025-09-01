from django.urls import path
from library.views import AddFavouriteBook, BookAddView, BookDeleteView, BookDetailView, BookEditView, BookListView, CategoryAdd, FavouriteBooks, RemoveFavouriteBook

urlpatterns = [
    path('book/', BookListView.as_view(), name="book-list"),
    path('book/add/', BookAddView.as_view(), name='book-add'),
    path('book/edit/<int:book_id>/', BookEditView.as_view(), name='book-edit'),
    path('book/detail/<int:book_id>/', BookDetailView.as_view(), name='book-detail'),
    path('book/delete/<int:book_id>/', BookDeleteView.as_view(), name='book-delete'),
    path('book/category/add/', CategoryAdd.as_view(), name="category-add"),
    path('book/favourite/', FavouriteBooks.as_view(), name='book-favourite'),
    path('book/favourite/add/<int:book_id>/', AddFavouriteBook.as_view(), name='book-favourite-add'),
    path('book/favourite/remove/<int:book_id>/', RemoveFavouriteBook.as_view(), name='book-favourite-remove'),
]

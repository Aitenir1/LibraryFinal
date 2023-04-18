from django.urls import path
from django.contrib.auth.decorators import login_required

from library.views import book, authentication, borrower, exemplar, borrow

from library.utils import clear_fine, end_borrow

urlpatterns = [
    # URLS for Authentication
    path(
        route='login',
        view=authentication.MyLoginView.as_view(),
        name='login'
    ),
    path(
        route='logout',
        view=login_required(authentication.MyLogoutView.as_view()),
        name='logout'
    ),


    # URLs for CRUD operators on Book
    path(
        route='',
        view=login_required(book.BooksListView.as_view()),
        name='home'
    ),
    path(
        route='book-detail/<str:pk>',
        view=login_required(book.BookDetailView.as_view()),
        name='book-detail'
    ),
    path(
        route='book-create',
        view=login_required(book.BookCreateView.as_view()),
        name='book-create'
    ),
    path(
        route='book-edit/<str:pk>',
        view=login_required(book.BookUpdateView.as_view()),
        name='book-edit'
    ),
    path(
        route='book-delete/<str:pk>',
        view=login_required(book.BookDeleteView.as_view()),
        name='book-delete'
    ),


    # URLs for CRUD operators on Borrower
    path(
        route='borrower-list',
        view=login_required(borrower.BorrowerListView.as_view()),
        name='borrower-list'
    ),
    path(
        route='borrower-detail/<str:pk>',
        view=login_required(borrower.BorrowerDetailView.as_view()),
        name='borrower-detail'
    ),
    path(
        route='borrower-create',
        view=login_required(borrower.BorrowerCreateView.as_view()),
        name='borrower-user'
    ),
    path(
        route='borrower-update/<str:pk>',
        view=login_required(borrower.BorrowerUpdateView.as_view()),
        name='borrower-update'
    ),


    # URLs for CRUD operators on Exemplar
    path(
        route='exemplar-list/<str:book>',
        view=login_required(exemplar.ExemplarListView.as_view()),
        name='exemplar-list'
    ),
    path(
        route='exemplar-detail/<str:pk>',
        view=login_required(exemplar.ExemplarDetailView.as_view()),
        name='exemplar-detail'
    ),
    path(
        route='exemplar-create/<str:book>',
        view=login_required(exemplar.ExemplarCreateView.as_view()),
        name='exemplar-create'
    ),


    # URLs for CRUD operators on Exemplar
    path(
        route='borrow-create/<str:exemplar>',
        view=login_required(borrow.BorrowCreateView.as_view()),
        name='borrow-create'
    ),


    # URLs for helper functions
    path(
        route='clear-fine/<str:pk>',
        view=login_required(clear_fine),
        name='clear-fine'
    ),
    path(
        route='end-borrow/<str:pk>',
        view=login_required(end_borrow),
        name='end-borrow'
    )

]



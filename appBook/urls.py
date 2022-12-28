from django.urls import path
from . import views

urlpatterns = [
    path('',views.form_page),
    path('register',views.register),
    path('login',views.login),
    path('addBook',views.addBook),
    path('viewBooksPage',views.viewBooksPage),
    path('editBook/<int:BookId>',views.editBook),
    path('viewBook/<int:BookId>',views.viewBook),
    path('likeBook/<int:BookId>',views.likeBook),
    path('update_desc_of_book/<int:BookId>',views.update_desc_of_book),
]
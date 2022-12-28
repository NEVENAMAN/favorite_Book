from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from .models import *

def form_page(request):
    return render(request,'index.html')

def register(request):
    print("***** 1 ")
    error = User.objects.basic_validator(request.POST)
    if len(error) > 0:
        print("***** 2 ")
        for key, value in error.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else:
        if request.method == "POST":
            print("***** 3 ")
            Register(request)
            print("***** 4 ")
        return redirect('/')

def login(request):
    if Login(request):
        return redirect('/viewBooksPage')
    

def viewBooksPage(request):
    id = request.session['userid'] 
    user = User.objects.get(id=id)
    # get all books from database
    book = Get_all_book(request)
    context = {
        "user" : user,
        "books" : book,
    }
    return render(request,'add_book.html',context)
# add book to books table
def addBook(request):
    error = Book.objects.book_validator(request.POST)
    if len(error) > 0:
        for key, value in error.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/viewBooksPage')
    else:
        if request.method == "POST":
            Add_Book(request)
        return redirect('/viewBooksPage')
# edit book data from own user
def editBook(request,BookId):
    id = request.session['userid'] 
    user = User.objects.get(id=id)
    book = Get_Book(BookId)
    user_who_like = Get_User_favorite_book(BookId)
    context = {
        "user" : user,
        "book" : book,
        "user_who_like" : user_who_like,
    }
    return render(request,'editBook.html',context)

# view book data page
def viewBook(request,BookId):
    id = request.session['userid'] 
    user = Get_User(id)
    book = Get_Book(BookId)
    user_who_like = Get_User_favorite_book(BookId)
    context = {
        "user" : user,
        "book" : book,
        "user_who_like" : user_who_like,
    }
    return render(request,'viewBook.html',context)


# add user who liked this book
def likeBook(request,BookId):
    UserId = request.session['userid'] 
    Like_Book(BookId,UserId)
    return redirect('/viewBook/'+str(BookId))
    
# update desc of book
def update_desc_of_book(request,BookId):
    if request.method == "POST":
        desc_edit = request.POST['desc_edit']
        Update_Desc_Book(BookId,desc_edit)
    return redirect('/editBook/'+str(BookId))


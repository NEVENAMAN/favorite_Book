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
    context = {
        "user" : user,
    }
    return render(request,'add_book.html',context)

def addBook(request):
    error = Book.objects.basic_validator(request.POST)
    if len(error) > 0:
        for key, value in error.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/viewBooksPage')
    else:
        if request.method == "POST":
            Add_Book(request)
        return redirect('/viewBooksPage')
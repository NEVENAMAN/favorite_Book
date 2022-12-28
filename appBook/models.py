import re
from django.db import models 
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        error = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        password_regex =re.compile(r'^[a-zA-Z0-9.+_-]')
        special_symbols = ['$','@','#','%','^','&']
        if len(postData['first_name']) < 3 :
            error['first_name'] = "first name should be at least 3 characters"
        if len(postData['last_name']) < 3 :
            error['last_name'] = "last name should be at least 3 characters"
        if not email_regex.match(postData['email']) :
            error['email'] = "invaild email"
        if len(postData['password']) < 6:
            error['password_less_than'] = "Password must have atleast 6 characters"
        if len(postData['password']) > 20 :
            error['password_grather_than'] = "'Password cannot have more than 20 characters"
        if not any(characters.isupper() for characters in postData['password']):
            error['password_notInclude_upper'] = "Password must have at least one uppercase character"
        if not any(characters.islower() for characters in postData['password']):
            error['password_notInclude_lower'] = "Password must have at least one lowercase character"
        if not any(characters.isdigit() for characters in postData['password']):
            error['password_notInclude_number'] = "Password must have at least one numeric character."
        if not any(characters in special_symbols for characters in postData['password']):
            error['password_symbol'] = "Password should have at least one of the symbols $@#%^&"
        
        return error
    def book_validator(self, postData):
        error = {}
        if len(postData['title']) < 1 :
            error['title'] = "title is required"
        if len(postData['desc']) < 5 :
            error['desc'] = "description should at least 5 characters"
        return error

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    upload_book = models.ForeignKey(User, related_name="upload_books", on_delete = models.DO_NOTHING)
    faverite_book = models.ManyToManyField(User, related_name="faverite_books" , default="")
    created_at=models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

def Register(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() 
    if (request.POST['confirm_password'] == password):
        return User.objects.create(first_name = first_name , last_name = last_name, email = email , password = pw_hash )

def Login(request):
    user = User.objects.filter(email = request.POST['email'])
    if user:
        loged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), loged_user.password.encode()):
            request.session['userid'] = loged_user.id
            return True
# add book to books tables
def Add_Book(request):
    title = request.POST['title']
    desc = request.POST['desc']
    upload_book = request.POST['upload_user_id']
    user = User.objects.get( id = upload_book)
    return Book.objects.create(title = title , desc = desc , upload_book = user )

def Get_all_book(request):
    return Book.objects.all()

def Get_User(id):
    return User.objects.get(id=id)

def Get_Book(BookId):
    return Book.objects.get(id = BookId)

# add user who liked this book
def Like_Book(BookId,UserId):
    book = Book.objects.get(id = BookId)
    user = User.objects.get(id = UserId)
    return book.faverite_book.add(user)

# get all user who liked this book
def Get_User_favorite_book(BookId):
    book = Book.objects.get(id = BookId)
    return book.faverite_book.all()

# update the description of book
def Update_Desc_Book(BookId,desc_edit):
    book = Book.objects.get(id = BookId)
    print("**** 1")
    book.desc == desc_edit
    print("***** 2")
    book.save()
    print("***** 3")
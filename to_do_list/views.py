from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from usersapp.models import Usertodo
from django.core.mail import EmailMessage,send_mail
import random
               
# Define a dictionary to store the OTPs temporarily

def submit(request):
        print(request.POST)
        
        if request.method == 'POST':
    
                first_name= request.POST.get('firstname')
                last_name= request.POST.get('lastname')
                password=request.POST.get('password')
                conform_password= request.POST.get('conform_password')
                email= request.POST.get('email')
                username= request.POST.get('username')
                user = User(email=email,first_name=first_name,last_name=last_name,username=username)
                user.set_password(password)
                user.save()
                 
                # subject = 'Your Registration Compleate'
                # message = f'Dear {username} '
                # from_email = email  
                # recipient_list = [email]
                # send_mail(subject, message, from_email,recipient_list)
                

                return redirect('/login')  

        return render(request,"index.html")

def my_login_func(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request,user)
            # print("Login successfull!")

            return redirect('/todolist_view')
        else:
            print(user)
            # print("Invalid login credentials.")
    
    return render(request, 'login.html')  # Adjust 'login.html' to your actual login template

def Todolist_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return render(request,"list.html")
         
    if request.method == "POST":
        if request.user.is_authenticated:
            print("debug2")
            user_id = request.user
            print("debug3")
            name=request.POST.get('name')
            title=request.POST.get('title')
            message=request.POST.get('message')
            print("debug4")

            Usertodo(user=user_id,title=title,message=message).save()
            print("debug5")
            return redirect('/todolist_view')
    else:
         return redirect("/login")

def Logout(request):
    
     auth.logout(request)
     return redirect("/login")

@login_required(login_url='/')
def listshow(request):
    print("dbug1")
    if request.method == "GET":
        todolists= Usertodo.objects.filter(user= request.user) 
        print(todolists)
        data= {"data": todolists}

        return render(request,'listshow.html',data)

def Delete(request,id):
     Usertodo.objects.get(id=id).delete()
     return redirect("/list_show")







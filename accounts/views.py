from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from .forms import RegisterForm



def registerPage(request):
    
    print(request.body)
    print(request.POST)
    
    if request.user.is_authenticated:
        return redirect("store")
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request , user)
            return redirect("store")
    context = {}
    return render(request , "accounts/register.html" , context)

def loginPage(request):
    
    if request.user.is_authenticated:
        return redirect("store")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        try:
            try:
                user = User.objects.get(email=username) 
            except:
                user = User.objects.get(username=username)
        except:
            messages.error(request , "user does not exist")
            return redirect("login")
            
    
        authenticated_user = authenticate(request , username=user.username , password=password)
    
        
    
    
        login(request , authenticated_user)
        return redirect("store")
        
    context ={}
    return render(request , "accounts/login.html" , context)

def logoutPage(request):
    logout(request)
    return redirect("store")
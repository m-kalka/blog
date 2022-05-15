from django.shortcuts import render
from .models import Post
from .forms import PostForm
import requests
from django.contrib.auth.decorators import login_required

from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse





#@login_required
def index(request):
    cytat = requests.get("https://api.chucknorris.io/jokes/random").json()
    form = PostForm(request.POST or None, initial={'user': request.user})
    if form.is_valid():
        form.save()
        return redirect("blog:index")
    posts = Post.objects.all().order_by('-id')
    return render(request,"blog.html", {
        'posts': posts,
        'form': form,
        'chuck': cytat
    }
    )

def navbar(request):
    return render(request,"base.html", {
        'posty': 'test'
    })
    
    
def register_request(request):
    invalid_register = ''

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            valid_register = "Rejestracja przebiegła pomyślnie"
            messages.success(request, valid_register)
            return redirect("blog:index")
        invalid_register = 'Rejestracja nie powiodła się. Nieprawidłowe informacje'
        messages.error(request, invalid_register)
    form = NewUserForm()
    return render (
        request=request, 
        template_name="register.html",
        context={
            "register_form":form,
            "register_invalid": invalid_register
            }
     )


def login_request(request):
    invalid_login = ''
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Zalogowałeś się jako {username}.")
                return redirect("blog:index")
            else:
                invalid_login = 'Nieprawidłowa nazwa użytkownika lub hasło.'
                messages.error(request, invalid_login)
        else:
            invalid_login = 'Nieprawidłowa nazwa użytkownika lub hasło.'
            messages.error(request, invalid_login)
    form = AuthenticationForm()
    return render(
        request=request,
        template_name="login.html",
        context={
            "login_form":form,
            "invalid_login": invalid_login
            }
        )


def logout_request(request):
	logout(request)
	messages.info(request, "Pomyślnie się wylogowałeś.") 
	return redirect("blog:index")


def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = "Uwagi dotyczące blogu" 
			body = {
			'first_name': form.cleaned_data['first_name'], 
			'last_name': form.cleaned_data['last_name'], 
			'email': form.cleaned_data['email_address'], 
			'message':form.cleaned_data['message'], 
			}
			message = "\n".join(body.values())

			try:
				send_mail(subject, message, 'admin@example.com', ['admin@example.com']) 
			except BadHeaderError:
				return HttpResponse('Znaleziono nieprawidłowy nagłówek.')
			return redirect ("blog:index")
      
	form = ContactForm()
	return render(request, "kontakt.html", {'form':form})
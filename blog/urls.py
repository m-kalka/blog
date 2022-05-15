from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('navbar', views.navbar, name='index2'),
    path('register', views.register_request, name='register'),
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name= 'logout'),
    path('kontakt', views.contact, name='kontakt'),
]

from django.urls import path

from . import views

# app_name = "antiscam"
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
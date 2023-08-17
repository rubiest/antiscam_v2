from django.urls import path

from . import views
from .views_auth import register, signin, signout, activate, edit_profile
from .views_dashboard import dashboard, profile, newscammer, search_create_scammer

# app_name = "antiscam"
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('scammer-lists/', views.scammerlist, name='scammerlist'),
    path('scammer-details/<int:scammer_id>', views.viewscammer, name='viewscammer'),
    #authentication
    path('register/', register, name='register'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('profile/edit', edit_profile, name='edit_profile'),
    #dashboard
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),
    path('scammers/new', newscammer, name='newscammer'),
    path('search_create_scammer/', search_create_scammer, name='search_create_scammer'),
]
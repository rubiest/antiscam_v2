from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views_auth import register, signin, signout, activate, edit_profile
from .views_dashboard import dashboard, profile, newscammer, search_create_scammer

# app_name = "antiscam"
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('scammer-lists/', views.scammerlist, name='scammerlist'),
    path('scammer-details/<int:scammer_id>', views.viewscammer, name='viewscammer'),
    path('scammer-details/<int:scammer_id>/case/new', views.newcase, name='newcase'),
    path('vote-unvote-scammer/<int:scammer_id>/', views.vote_unvote_scammer, name='vote-unvote-scammer'),
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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
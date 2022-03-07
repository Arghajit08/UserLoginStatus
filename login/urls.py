from re import U
from django.urls import path
from .views import UserProfile,UserLogin,UserLogout

urlpatterns = [
    path('create', UserProfile.as_view()),
    path('login', UserLogin.as_view()),
    path('logout', UserLogout.as_view()),
    
]
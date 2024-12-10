from django.contrib import admin
from django.urls import path, include

from .views import RegisterAPIView, LoginAPIView, UserAPIView, LogoutAPIView, ProfileInfoView, ProfilePasswordAPIView

urlpatterns = [
    path('register', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('user', UserAPIView.as_view()),
    path('logout', LogoutAPIView.as_view()),
    path('users/info', ProfileInfoView.as_view()),
    path('users/password', ProfileInfoView.as_view())
]

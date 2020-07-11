from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("signout/", auth_views.LogoutView.as_view(), name="signout"),
]

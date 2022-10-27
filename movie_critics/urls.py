from django.urls import path

from . import views

urlpatterns = [
    path("users/register/", views.ResgisterUser.as_view()),
    path("users/", views.UserView.as_view()),
    path("users/<int:user_id>/", views.UserDetailView.as_view()),
    path("users/login/", views.LoginUser.as_view()),
]

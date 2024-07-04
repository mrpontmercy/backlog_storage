from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.login_user, name="login"),
    # path("logout/", views.logout_user, name="logout"),
    path("logout/", views.logout_user, name="logout"),
    path("registration/", views.register, name="registration"),
]

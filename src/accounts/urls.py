from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('send_login_email', views.send_login_email, name='send-login-email'),
    path('login', views.login, name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page="/"), name='logout'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('members/', views.members, name='members'),
    path('members/login_user', views.login_user, name='login_user'),
    path('members/logout_user', views.logout_user, name='logout_user'),
    path('members/profile', views.profile, name='profile' ),
]


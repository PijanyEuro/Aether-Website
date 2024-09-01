from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('shop/', views.shop, name='shop'),
    path('members/', views.members, name='members'),
    path('members/login_user', views.login_user, name='login_user'),
    path('members/logout_user', views.logout_user, name='logout_user'),
    path('members/profile', views.profile, name='profile'),
    path('members/profile/edit/', views.profile_edit, name='profile_edit'),
    path('members/characters/add/', views.add_character, name='add_character'),
    path('members/characters/edit/<int:character_id>/', views.edit_character, name='edit_character'),
    path('members/characters/', views.characters, name='characters'),
    path('members/inventory/', views.inventory, name='inventory'),
    path('members/inventory/add_item/', views.add_item, name='add_item'),
    path('members/inventory/create_item/', views.create_item, name='create_item'),  # This line should be for creating new
    path('members/inventory/edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
]

from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name='main'),
    path('shop/', views.shop, name='shop'),
    path('join_event/<int:event_id>/', views.join_event, name='join_event'),
    path('members/events/', views.events_page, name='events_page'),
    path('members/', views.members, name='members'),
    path('members/login_user', views.login_user, name='login_user'),
    path('members/logout_user', views.logout_user, name='logout_user'),
    path('members/profile', views.profile, name='profile'),
    path('members/profile/edit/', views.profile_edit, name='profile_edit'),
    path('members/characters/add/', views.add_character, name='add_character'),
    path('members/characters/edit/<int:character_id>/', views.edit_character, name='edit_character'),
    path('members/my_characters/', views.my_characters, name='my_characters'),
    path('members/all_characters/', views.all_characters, name='all_characters'),
    path('members/inventory/', views.inventory, name='inventory'),
    path('members/inventory/add_item/', views.add_item, name='add_item'),
    path('members/inventory/create_item/', views.create_item, name='create_item'),  # This line should be for creating new
    path('members/inventory/edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('open_lootbox/<int:item_id>/', views.open_lootbox, name='open_lootbox'),
]

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from functools import wraps
from datetime import date

from .models import SeasonalContent, Profile, Character, Item, Bundle, ShopItem, ProfileItem
from .forms import CharacterForm, ProfileForm, AddItemForm, CreateItemForm, ItemForm

# Create your views here.

def main(request):
    today = date.today()
    seasonal_content_entries = SeasonalContent.objects.filter(start_date__lte=today, end_date__gte=today)
    
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        
    return render(request, 'index.html', {
        'seasonal_content_entries': seasonal_content_entries,
        'profile': profile
    })

def members(request):
    return HttpResponse("Hello world!")

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, "There was an error logging in, try again.")
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('main')

def login_required_with_message(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to view this page.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'profile.html', {'profile': profile})

@login_required
def profile_edit(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = ProfileForm(instance=profile)
    
    return render(request, 'profile_edit.html', {'profile_form': profile_form})

@login_required
def add_character(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = CharacterForm(request.POST, request.FILES)
        if form.is_valid():
            character = form.save(commit=False)
            character.profile = profile
            character.save()
            profile.characters.add(character)
            return redirect('characters')
    else:
        form = CharacterForm()
    
    return render(request, 'add_character.html', {'form': form})

@login_required
def edit_character(request, character_id):
    profile = get_object_or_404(Profile, user=request.user)
    character = get_object_or_404(Character, id=character_id, profile=profile)
    if request.method == 'POST':
        form = CharacterForm(request.POST, request.FILES, instance=character)
        if form.is_valid():
            form.save()
            return redirect('characters')
    else:
        form = CharacterForm(instance=character)
    
    return render(request, 'edit_character.html', {'form': form, 'character': character})

@login_required
def characters(request):
    profile = get_object_or_404(Profile, user=request.user)
    characters = profile.characters.all()
    return render(request, 'characters.html', {'characters': characters, 'profile': profile})

@login_required
def add_item(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = AddItemForm(request.POST)
        if form.is_valid():
            item_id = form.cleaned_data['item'].id
            quantity = form.cleaned_data['quantity']
            item = get_object_or_404(Item, id=item_id)
            
            profile_item, created = ProfileItem.objects.get_or_create(profile=profile, item=item)
            if not created:
                profile_item.quantity += quantity
            else:
                profile_item.quantity = quantity
            profile_item.save()
            
            return redirect('inventory')
    else:
        form = AddItemForm()
    
    return render(request, 'add_item.html', {'form': form})

@login_required
def create_item(request):
    if request.method == 'POST':
        form = CreateItemForm(request.POST, request.FILES)
        if form.is_valid():
            new_item = form.save()
            profile = Profile.objects.get(user=request.user)
            ProfileItem.objects.create(profile=profile, item=new_item, quantity=1)
            return redirect('inventory')
    else:
        form = CreateItemForm()
    
    return render(request, 'create_item.html', {'form': form})

@login_required
def edit_item(request, item_id):
    profile = get_object_or_404(Profile, user=request.user)
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('inventory')
    else:
        form = ItemForm(instance=item)
    
    return render(request, 'edit_item.html', {'form': form, 'item': item})

@login_required
def inventory(request):
    profile = get_object_or_404(Profile, user=request.user)
    profile_items = ProfileItem.objects.filter(profile=profile)
    return render(request, 'inventory.html', {'profile': profile, 'items': profile_items})

@login_required
def shop(request):
    profile = get_object_or_404(Profile, user=request.user)
    shop_items = ShopItem.objects.all()
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        shop_item = get_object_or_404(ShopItem, id=item_id)
        
        if shop_item.quantity > 0 and profile.essence_count >= shop_item.price:
            profile.essence_count -= shop_item.price
            profile.save()
            
            profile_item, created = ProfileItem.objects.get_or_create(profile=profile, item=shop_item.item)
            if not created:
                profile_item.quantity += 1
            else:
                profile_item.quantity = 1
            profile_item.save()
            
            shop_item.quantity -= 1
            shop_item.save()
            
            messages.success(request, "Purchase successful!")
        else:
            messages.error(request, "Not enough essence or item sold out.")
        
        return redirect('shop')
    
    return render(request, 'shop.html', {'shop_items': shop_items, 'profile': profile})

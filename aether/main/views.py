from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from .models import SeasonalContent, Profile, Character, Set, Item, Bundle
from datetime import date
# Create your views here.



def main(request):
        
    today = date.today()
    SeasonalContentEntries = SeasonalContent.objects.filter(start_date__lte=today).filter(end_date__gte=today)
    return render(request, 'index.html', {'SeasonalContentEntries': SeasonalContentEntries})


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
def members(request):
    return HttpResponse("Hello world!")

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('main')
        else:
            # Return an 'invalid login' error message.
            messages.success(request, "There was an error logging in, try again....")
            return redirect('main')
    else:
        return render(request, 'authenticate/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('main')

def login_required_with_message(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.success(request, "You must be logged in to view this page.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)# Get the user's profile
    characters = profile.characters.all()# Get the related characters and items
    items = profile.inventory.all()
    context = {
        'profile': profile,
        'characters': characters,
        'items': items,
    }# Pass the data to the template
    
    return render(request, 'profile.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile, Character, Item
from .forms import ProfileForm, CharacterForm, ItemForm

@login_required
def profile_edit(request):
    profile = get_object_or_404(Profile, user=request.user)
    
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        character_forms = [CharacterForm(request.POST, request.FILES, instance=character) for character in profile.characters.all()]
        item_forms = [ItemForm(request.POST, request.FILES, instance=item) for item in profile.inventory.all()]

        if all(form.is_valid() for form in [profile_form] + character_forms + item_forms):
            profile_form.save()
            for form in character_forms:
                form.save()
            for form in item_forms:
                form.save()
            return redirect('profile')  # Redirect to profile view after saving
    else:
        profile_form = ProfileForm(instance=profile)
        character_forms = [CharacterForm(instance=character) for character in profile.characters.all()]
        item_forms = [ItemForm(instance=item) for item in profile.inventory.all()]
    
    context = {
        'profile_form': profile_form,
        'character_forms': character_forms,
        'item_forms': item_forms,
    }

    
    
    return render(request, 'profile_edit.html', context)

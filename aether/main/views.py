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



from django.shortcuts import render
from .models import Profile
from django.contrib.auth.decorators import login_required

def main(request):
    today = date.today()
    SeasonalContentEntries = SeasonalContent.objects.filter(start_date__lte=today).filter(end_date__gte=today)
    
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        
    return render(request, 'index.html', {
        'SeasonalContentEntries': SeasonalContentEntries,
        'profile': profile
    })


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
    context = {
        'profile': profile,
    }# Pass the data to the template
    
    return render(request, 'profile.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm

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

    context = {
        'profile_form': profile_form,
    }

    return render(request, 'profile_edit.html', context)




@login_required
def add_character(request):
    profile = get_object_or_404(Profile, user=request.user)
    
    if request.method == 'POST':
        form = CharacterForm(request.POST, request.FILES)
        if form.is_valid():
            character = form.save(commit=False)
            character.profile = profile  # Associate the character with the profile
            character.save()
            profile.characters.add(character)  # Ensure the character is added to the profile's characters
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
    
    context = {
        'characters': characters,
        'profile': profile,
    }
    
    return render(request, 'characters.html', context)


@login_required
def add_item(request):
    profile = get_object_or_404(Profile, user=request.user)
    
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()  # Save item first
            profile.inventory.add(item)  # Associate item with profile
            return redirect('inventory')
    else:
        form = ItemForm()

    return render(request, 'add_item.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile, Item
from .forms import ItemForm

@login_required
def edit_item(request, item_id):
    profile = get_object_or_404(Profile, user=request.user)
    item = get_object_or_404(Item, id=item_id)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('inventory')  # Redirect to inventory or another appropriate page
    else:
        form = ItemForm(instance=item)

    context = {
        'form': form,
        'item': item,
    }

    return render(request, 'edit_item.html', context)


@login_required
def inventory(request):
    profile = Profile.objects.get(user=request.user)
    items = profile.inventory.all()
    
    context = {
        'items': items,
        'profile': profile,
    }
    
    return render(request, 'inventory.html', context)

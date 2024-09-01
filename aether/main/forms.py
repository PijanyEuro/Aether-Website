from django import forms
from .models import Profile, Character, Item

from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'profile_name']
        widgets = {
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
            'profile_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'profile_pic': 'Profile Picture',
            'profile_name': 'Profile Name',
        }


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['top_down_photo', 'character_name', 'character_class', 'level', 'strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma', 'bio']
        widgets = {
            'top_down_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'character_name': forms.TextInput(attrs={'class': 'form-control'}),
            'character_class': forms.TextInput(attrs={'class': 'form-control'}),  # Changed to TextInput
            'level': forms.NumberInput(attrs={'class': 'form-control'}),
            'strength': forms.NumberInput(attrs={'class': 'form-control'}),
            'dexterity': forms.NumberInput(attrs={'class': 'form-control'}),
            'constitution': forms.NumberInput(attrs={'class': 'form-control'}),
            'intelligence': forms.NumberInput(attrs={'class': 'form-control'}),
            'wisdom': forms.NumberInput(attrs={'class': 'form-control'}),
            'charisma': forms.NumberInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'top_down_photo': 'Top Down Photo',
            'character_name': 'Character Name',
            'character_class': 'Character Class',
            'level': 'Level',
            'strength': 'Strength',
            'dexterity': 'Dexterity',
            'constitution': 'Constitution',
            'intelligence': 'Intelligence',
            'wisdom': 'Wisdom',
            'charisma': 'Charisma',
            'bio': 'Character Bio',
        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['image', 'item_name', 'description']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'image': 'Item Image',
            'item_name': 'Item Name',
            'description': 'Item Description',
        }

# forms.py

from django import forms
from .models import Item

class AddItemForm(forms.Form):
    item = forms.ModelChoiceField(
        queryset=Item.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    quantity = forms.IntegerField(
        min_value=1,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

class CreateItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'description', 'image']
        widgets = {
            'item_name': forms.Textarea(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
from django.contrib import admin
from .models import Member, Profile, SeasonalContent, Item, Character, Set, Bundle

class ItemInline(admin.TabularInline):
    model = Profile.inventory.through
    extra = 1

class CharacterInline(admin.TabularInline):
    model = Profile.characters.through
    extra = 1

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'profile_pic', 'name', 'essence_count')  # Exclude inventory and characters here
    inlines = [ItemInline, CharacterInline]

admin.site.register(Member)
admin.site.register(Item)
admin.site.register(Character)
admin.site.register(Set)
admin.site.register(Bundle)

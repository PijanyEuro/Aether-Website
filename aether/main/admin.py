from django.contrib import admin
from .models import Member, Profile, SeasonalContent, Item, Character, Set, Bundle, ShopItem, ProfileItem




admin.site.register(Member)
admin.site.register(Item)
admin.site.register(Character)
admin.site.register(Set)
admin.site.register(Bundle)
admin.site.register(ShopItem)
admin.site.register(ProfileItem)

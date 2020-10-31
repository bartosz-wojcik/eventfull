from django.contrib import admin
from website_pages.models import Event
from website_pages.models import Order
from website_pages.models import Category
from website_pages.models import WishList
from website_pages.models import Promotion
from website_pages.models import UserProfile
from django.contrib.auth.admin import UserAdmin


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(Order)
admin.site.register(WishList)
admin.site.register(Promotion)
admin.site.register(Category)


# @admin.register(UserAdmin)
# class CustomUserAdmin(UserProfile):
#     list_display = (
#         'id', 'first_name', 'last_name', 'username', 'email'
#     )




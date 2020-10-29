from django.db import models
from django.contrib.auth.models import AbstractUser

USER_TYPES = (
    ('u', 'user'),
    ('p', 'promoter'),
)


class Category(models.Model):
    name = models.CharField(max_length=80),
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


# inheriting from built in abstract user that has all the fields already defined
class UserProfile(AbstractUser):
    user_type = models.CharField(max_length=1, choices=USER_TYPES, default=USER_TYPES[0][0], blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Event(models.Model):
    promoter = models.ForeignKey('website_pages.UserProfile', on_delete=models.CASCADE)
    category = models.ForeignKey('website_pages.Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=400)
    venue_name = models.CharField(max_length=200)
    performer_names = models.CharField(max_length=400)
    ticket_price = models.DecimalField(max_digits=6, decimal_places=2)
    ticket_quantity = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Promotion(models.Model):
    promoter = models.ForeignKey('website_pages.UserProfile', on_delete=models.CASCADE)
    event= models.ForeignKey('website_pages.Event', on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.CharField(max_length=400)
    promo_code = models.CharField(max_length=8)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Order(models.Model):
    promoter = models.ForeignKey('website_pages.UserProfile', on_delete=models.CASCADE)
    event = models.ForeignKey('website_pages.Event', on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    ticket_amount = models.DecimalField(max_digits=8, decimal_places=2)
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2)
    ticket_quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class WishList(models.Model):
    user = models.ForeignKey('website_pages.UserProfile', on_delete=models.CASCADE)
    event = models.ForeignKey('website_pages.Event', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)



















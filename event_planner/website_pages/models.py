from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django import forms


class Categories(models.Model):
    name = models.CharField(max_length=80),
    created_on = models.DateField()
    modified_on = models.DateField();

# class User(models.Model):
#     type = (
#         ('u', 'user'),
#         ('p', 'promoter'),
#     )
#     first_name = models.CharField(max_length=40),
#     last_name = models.CharField(max_length=40),
#     email = models.EmailField(max_length=254),
#



class Events(models.Model):
    CategoryId = models.ForeignKey(Categories, related_name='id'),
    name = models.CharField(max_length=40),
    date = models.DateField()




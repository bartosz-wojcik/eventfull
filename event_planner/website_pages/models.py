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

# class Events(models.Model):
#     CategoryId = models.ForeignKey(Category, related_name='id'),
#     name = models.CharField(max_length=40, ),
#     date = models.DateField()






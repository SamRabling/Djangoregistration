from __future__ import unicode_literals

from django.db import models
from django.views import View
import bcrypt
import re

EMAILREGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class RegistrationManager(models.Manager):
    def regis_basic_validator(self, postData):
        errors={}
        if len(postData['first_name']) < 5:
            errors['first_name'] = "Your name should be more than 5 characters"
        if len(postData['last_name']) < 5:
            errors['last_name'] = "Your last name should be more than 5 characters"
        if not EMAILREGEX.match(postData['email']):
            errors['email'] = "Your email needs to have the correct format."
        if len(postData['Password']) < 8:
            errors['Password'] = "Your password needs to be at least 8 characters"
        if postData['confirm_pw'] != postData['Password']:
            errors['confirm_pw'] = "Your passwords need to match"
        if postData['birthday'] == 1900-01-01:
            errors['birthday'] = "Please enter a valid date"
        if User.objects.filter(email=postData['email']) == []:
            error['ex_email'] = "You already have an account"
        return errors
    def log_basic_validator(self, postData):
        errors ={}
        if not EMAILREGEX.match(postData['email']):
            errors['email'] = "Your email needs to have the correct format."
        password = User.objects.get(email=postData['email']).password
        print password
        if bcrypt.checkpw(postData['Password'].encode(), password.encode()) != True:
            errors['Password'] = "Please revise your email and password"
        return errors
    def item_basic_validator(self, postData):
        errors={}
        if len(postData['name']) < 3:
            errors['name'] = "The item name should be more than 3 characters"
        return errors
        
class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length=255)
    birthday = models.DateField(default = 12-12-1999)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = RegistrationManager()
    def __str__(self):
        return "<User objects: {} {} {} {}>". format(self.first_name, self.last_name, self.email, self.created_at)

class Item(models.Model):
    name = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    owner = models.ForeignKey(User, related_name = "wisher")
    wishlist = models.ManyToManyField(User, related_name="wished")
    objects = RegistrationManager()
    def __str__(self):
        return "<Item objects: {} {} {}>". format(self.name, self.created_at, self.wishlist)



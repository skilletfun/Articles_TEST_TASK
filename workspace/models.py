from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=16, unique=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Article(models.Model):
    name = models.CharField(max_length=16)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    categories = models.ManyToManyField(Category)
    content = models.CharField(max_length=255)
    link = models.CharField(max_length=64)
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)


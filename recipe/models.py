from django.db import models

from user.models import User


class Recipe(models.Model):
    name = models.CharField(max_length=100, default='')
    url = models.CharField(max_length=255, default='', blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class MealType(models.Model):
    name = models.CharField(max_length=100, default='')
    slug = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name


class Meal(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    date_added = models.DateTimeField(auto_now_add=True)
    
    day = models.DateField()
    type = models.ForeignKey(MealType, on_delete=models.PROTECT)


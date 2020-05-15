from django.contrib import admin


from .models import Meal, MealType, Recipe


admin.site.register(Meal)
admin.site.register(MealType)
admin.site.register(Recipe)
from rest_framework import serializers

from recipe.models import Meal, MealType, Recipe
from user.models import User


class MealTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealType
        fields = ['id', 'name']


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'url']


class MealSerializer(serializers.ModelSerializer):
    type = MealTypeSerializer(many=False, read_only=True)
    recipe = RecipeSerializer(many=False, read_only=True)

    class Meta:
        model = Meal
        fields = ['id', 'date_added', 'day', 'type', 'recipe']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']
from rest_framework import serializers

from recipe.models import Meal, MealType, Recipe
from user.models import User


class MealTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealType
        fields = ['id', 'name', 'slug']


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'url', 'user']
        extra_kwargs = {
            'user': {'write_only': True},
        }


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['id', 'date_added', 'day', 'type', 'recipe', 'user']
        extra_kwargs = {
            'user': {'write_only': True},
        }

    def to_representation(self, instance):
        self.fields['type'] =  MealTypeSerializer(many=False, read_only=True)
        self.fields['recipe'] =  RecipeSerializer(many=False, read_only=True)

        return super(MealSerializer, self).to_representation(instance)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']
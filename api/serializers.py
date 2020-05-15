from rest_framework import serializers


from recipe.models import Meal, MealType
from user.models import User

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'


class MealTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealType
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
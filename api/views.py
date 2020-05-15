from django.http import Http404

from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipe.models import Meal, MealType

from .serializers import MealSerializer, MealTypeSerializer


class index(APIView):
    def get(self, request, format=None):
        return Response({'message': 'abc'})


class mealList(APIView):
    def get(self, request, format=None):
        meals = Meal.objects.all() #filter(user=request.user)
        serialiser = MealSerializer(meals, many=True)
        return Response(serialiser.data)

    def post(self, request, format=None):
        data = request.data
        #data['user'] = request.user.id
        serialiser = MealSerializer(data=data)

        if serialiser.is_valid():
            serialiser.save()
        else:
            return Response(serialiser.errors)

        return Response(serialiser.data)


class mealDetail(APIView):
    def get_object(self, pk):
        try:
            return Meal.objects.get(id=pk)
        except Meal.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        meal = self.get_object(pk=pk)

        if request.method == 'DELETE':
            meal.delete()
            return Response({
                "ok": "ok"
            })

    def get(self, request, pk, format=None):
        meal = self.get_object(pk=pk)
        
        serialiser = MealSerializer(meal, many=False)
        return Response(serialiser.data)

    def post(self, request, pk, format=None):
        meal = self.get_object(pk=pk)

        serializer = MealSerializer(instance=meal, data=request.data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serialiser.errors)

        return Response(serializer.data)


class mealTypeList(APIView):
    def get(self, request, format=None):
        types = MealType.objects.all()
        serialiser = MealTypeSerializer(types, many=True)
        return Response(serialiser.data)

    def post(self, request, format=None):
        serialiser = MealTypeSerializer(data=request.data)

        if serialiser.is_valid():
            serialiser.save()
        else:
            return Response(serialiser.errors)

        return Response(serialiser.data)


class mealTypeDetail(APIView):
    def get_object(self, pk):
        try:
            return MealType.objects.get(id=pk)
        except MealType.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        type = self.get_object(pk=pk)
        serialiser = MealTypeSerializer(type, many=False)
        return Response(serialiser.data)

    def delete(self, request, pk, format=None):
        type = self.get_object(pk=pk)

        if request.method == 'DELETE':
            type.delete()
            return Response({
                "ok": "ok"
            })

    def post(self, request, pk, format=None):
        type = self.get_object(pk=pk)

        serializer = MealTypeSerializer(instance=type, data=request.data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serialiser.errors)

        return Response(serializer.data)
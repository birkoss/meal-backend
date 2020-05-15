from rest_framework.decorators import api_view
from rest_framework.response import Response

from recipe.models import Meal

from .serializers import MealSerializer

@api_view(['GET'])
def index(request):
    return Response({'message': 'abc'})


@api_view(['GET', 'POST'])
def mealList(request):
    if request.method == 'POST':
        data = request.data
        #data['user'] = request.user.id
        serialiser = MealSerializer(data=data)

        if serialiser.is_valid():
            serialiser.save()
        else:
            return Response(serialiser.errors)

        return Response(serialiser.data)
    else:
        meals = Meal.objects.all() #filter(user=request.user)
        serialiser = MealSerializer(meals, many=True)
        return Response(serialiser.data)


@api_view(['GET', 'POST', 'DELETE'])
def mealDetail(request, pk):
    meal = Meal.objects.get(id=pk)

    if request.method == 'DELETE':
        meal.delete()
        return Response({
            "ok": "ok"
        })
    elif request.method == 'POST':
        serializer = MealSerializer(instance=meal, data=request.data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serialiser.errors)

        return Response(serializer.data)
    else:
        serialiser = MealSerializer(meal, many=False)
        return Response(serialiser.data)
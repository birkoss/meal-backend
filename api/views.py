from django.contrib.auth import login, authenticate
from django.db.models import Q

from rest_framework import authentication, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from recipe.models import Meal, MealType, Recipe
from user.models import User

from .serializers import MealSerializer, MealTypeSerializer, RecipeSerializer, UserSerializer


class index(APIView):
    def get(self, request, format=None):
        return Response({'message': 'abc'})


class userLogin(APIView):
    def post(self, request, format=None):

        user = authenticate(request, email=request.data['email'], password=request.data['password'])
        if user is not None:
            login(request, user)

            token = Token.objects.get(user=user)

            return Response({
                'status': status.HTTP_200_OK,
                'item': request.data,
                'token': token.key,
            })
        else:
            return ResponseApiError()


class userRegister(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.create_user(
                serializer.data['email'],
                request.data['password']
            )

            token = Token.objects.get(user=user)

            return Response({
                'status': status.HTTP_200_OK,
                'item': serializer.data,
                'token': token.key,
            })
        else:
            return ResponseApiSerializerError(serializer)


class mealList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):

        filters = Q()
        filters.add(Q(user=request.user), Q.AND)

        date_start = request.GET.get('start', None)
        if date_start:
            filters.add(Q(day__gte=date_start), Q.AND)

        date_end = request.GET.get('end', None)
        if date_end:
            filters.add(Q(day__lte=date_end), Q.AND)

        meals = Meal.objects.filter(filters).order_by('day')
        serialiser = MealSerializer(meals, many=True)
        return Response({
            'status': status.HTTP_200_OK,
            'items': serialiser.data,
        })

    def post(self, request, format=None):
        data = request.data
        data['user'] = request.user.id

        serialiser = MealSerializer(data=data)
        print(data)
        if serialiser.is_valid():
            serialiser.save()
        else:
            return ResponseApiSerializerError(serialiser)

        return Response({
            'status': status.HTTP_200_OK,
            'item': serialiser.data,
        })


class mealDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        #print(rest_framework.status.HTTP_404_NOT_FOUND)
        try:
            return Meal.objects.get(id=pk)
        except Meal.DoesNotExist:
            return None

    def delete(self, request, pk, format=None):
        meal = self.get_object(pk=pk)

        if meal is None:
            return ResponseApiError(status.HTTP_404_NOT_FOUND)

        if meal.user.id is not request.user.id:
            return ResponseApiError()

        if request.method == 'DELETE':
            meal.delete()
            return Response({
                "status": status.HTTP_200_OK
            })

    def get(self, request, pk, format=None):
        meal = self.get_object(pk=pk)

        if meal is None:
            return ResponseApiError(status.HTTP_404_NOT_FOUND)

        if meal.user.id is not request.user.id:
            return ResponseApiError()
        
        serialiser = MealSerializer(meal, many=False)
        return Response({
            "status": status.HTTP_200_OK, 
            "item": serialiser.data
        })

    def post(self, request, pk, format=None):
        meal = self.get_object(pk=pk)

        if meal is None:
            return ResponseApiError(status.HTTP_404_NOT_FOUND)

        if meal.user.id is not request.user.id:
            return ResponseApiError()

        data = request.data
        data['user'] = request.user.id

        serializer = MealSerializer(instance=meal, data=data)

        if serializer.is_valid():
            serializer.save()
        else:
            return ResponseApiSerializerError(serializer)

        return Response({
            "status": status.HTTP_200_OK,
            "item": serializer.data,
        })


class mealTypeList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    # https://stackoverflow.com/questions/35970970/django-rest-framework-permission-classes-of-viewset-method

    def get(self, request, format=None):
        types = MealType.objects.all()
        serialiser = MealTypeSerializer(types, many=True)
        return Response({
            'status': status.HTTP_200_OK,
            'items': serialiser.data
        })

    # def post(self, request, format=None):
    #     serialiser = MealTypeSerializer(data=request.data)

    #     if serialiser.is_valid():
    #         serialiser.save()
    #     else:
    #         return ResponseApiSerializerError(serializer)

    #     return Response(serialiser.data)


class mealTypeDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

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
                status: status.HTTP_200_OK
            })

    def post(self, request, pk, format=None):
        type = self.get_object(pk=pk)

        serializer = MealTypeSerializer(instance=type, data=request.data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serialiser.errors)

        return Response(serializer.data)


class recipeList(APIView):
    def post(self, request, format=None):
        data = request.data
        data['user'] = request.user.id

        serialiser = RecipeSerializer(data=data)
        if serialiser.is_valid():
            serialiser.save()
        else:
            return ResponseApiSerializerError(serialiser)

        return Response({
            'status': status.HTTP_200_OK,
            'item': serialiser.data,
        })


class recipeSearch(APIView):
    def get(self, request, format=None):
        print( request.GET.get('search') )
        if request.GET.get('search'):
            recipes = Recipe.objects.filter(name__contains=request.GET.get('search'))

            serializer = RecipeSerializer(recipes, many=True)

            return Response({
                'status': status.HTTP_200_OK,
                'items': serializer.data,
            })
        
        return ResponseApiError(status.HTTP_400_BAD_REQUEST)


def ResponseApiError(status_code=status.HTTP_401_UNAUTHORIZED):
    message = {
        "status": status_code,
        "title": "Unauthorized",
        "message": "The request has not been applied because it lacks valid authentication credentials for the target resource."
    }

    if status_code == status.HTTP_404_NOT_FOUND:
        message['title'] = "Not Found"
        message['message'] = "The request has not been found."
    elif status_code == status.HTTP_400_BAD_REQUEST:
        message['title'] = "Bad Request"
        message['message'] = "The request is not valid."

    return Response(message, status=status_code)


def ResponseApiSerializerError(serializer, status_code=status.HTTP_400_BAD_REQUEST):
    message = {
        "status": status_code,
        "title": "Bad Request",
        "message": ""
    }

    for field in serializer.errors:
        for error in serializer.errors[field]:
            message['message'] += field + " : " + error + "\n"

    return Response(message, status=status_code)
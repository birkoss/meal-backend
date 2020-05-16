from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from . import views


urlpatterns = [
    path('', views.index.as_view(), name="api-index"),

    path('meals/', views.mealList.as_view(), name="api-meal-list"),
    path('meals/<str:pk>/', views.mealDetail.as_view(), name="api-meal-detail"),

    path('meal-types/', views.mealTypeList.as_view(), name="api-meal-type-list"),
    path('meal-types/<str:pk>/', views.mealTypeDetail.as_view(), name="api-meal-type-detail"),

    path('-token-auth/', obtain_auth_token, name='api-token-auth'),
    path('register/', views.userRegister.as_view(), name='api-register'),
    path('login/', views.userLogin.as_view(), name='api-login'),
]
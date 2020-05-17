from django.urls import path

from . import views


urlpatterns = [
    path('', views.index.as_view(), name="api-index"),

    path('meals/', views.mealList.as_view(), name="api-meal-list"),
    path('meals/<str:pk>/', views.mealDetail.as_view(), name="api-meal-detail"),

    path('recipes/', views.recipeList.as_view(), name="api-recipe-list"),
    path('recipes/search/', views.recipeSearch.as_view(), name="api-recipe-search"),

    path('meal-types/', views.mealTypeList.as_view(), name="api-meal-type-list"),
    path('meal-types/<str:pk>/', views.mealTypeDetail.as_view(), name="api-meal-type-detail"),

    path('register/', views.userRegister.as_view(), name='api-register'),
    path('login/', views.userLogin.as_view(), name='api-login'),
]
from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name="api-index"),

    path('meals/', views.mealList, name="api-meal-list"),
    path('meals/<str:pk>/', views.mealDetail, name="api-meal-detail"),

    path('meal-types/', views.mealTypeList, name="api-meal-type-list"),
    path('meal-types/<str:pk>/', views.mealTypeDetail, name="api-meal-type-detail"),
]
from django.contrib import admin
from restaurant_app.views import *
from django.urls import path
from django.urls import path






urlpatterns = [
    path('admin/', admin.site.urls),
    path('categories/', CategoryAPIView.as_view()),
    path('categories/<int:pk>/', CategoryAPIView.as_view()),
    path('dishes/', DishesAPIView.as_view()),
    path('dishes/<int:pk>/', DishesAPIView.as_view()),
    path('drinks/', DrinksAPIView.as_view()),
    path('deliveries/', DeliveryAPIView.as_view()),
    path('deliveries/<int:pk>/', DeliveryAPIView.as_view()),
    path('search_dishes/', SearchDishesApiView.as_view()),
    path('new_dishes/', NewDishesApiView.as_view()),
    path('random-recipe/', RandomRecipeApiView.as_view()),
    path('auth', AuthApiView.as_view()),
    path('reg', RegistrationApiView.as_view()),
    path('cab', UserCabinetApiView.as_view()),
    path('paginator', DishesPaginatedApiView.as_view()),
]

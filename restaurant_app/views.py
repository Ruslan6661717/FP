from http.client import responses

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from .serializers import *


# напитки
class DrinksAPIView(APIView):
    def get(self, request):
        drinks = Drinks.objects.all()
        data = DrinksSerializer(drinks, many=True)
        return Response(data=data, status=status.HTTP_200_OK)


# доставка
class DeliveryAPIView(APIView):
    def get(self, request):
        deliveries = Delivery.objects.all()
        data = DeliverySerializer(deliveries, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DeliverySerializer(data=request.data)
        if serializer.is_valid():
            # сделал доставку
            delivery = serializer.save()

            # считываю общую стоимость доставки
            delivery.calculate_total_price()

            return Response(DeliverySerializer(delivery).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # postman http://127.0.0.1:8000/deliveries/


from rest_framework.permissions import BasePermission


class VipUser(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PATCH', 'DELETE']:
            if request.user and request.user.is_staff:
                return True
            else:
                return False
        else:
            return True


class CategoryAPIView(APIView):
    permission_classes = [VipUser]

    def get(self, request):
        categories = Category.objects.all()
        data = CategorySerializer(instance=categories, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request):
        new_category = CategorySerializer(data=request.data)
        if new_category.is_valid():
            new_category.save()
            return Response(data={'message': 'Category Created!'}, status=status.HTTP_200_OK)
        else:
            return Response(data=new_category.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        category = Category.objects.get(pk=pk)
        updated_category = CategorySerializer(category, data=request.data, partial=True)
        if updated_category.is_valid():
            updated_category.save()
            return Response(data={'message': 'Category Updated!'}, status=status.HTTP_200_OK)
        return Response(data=updated_category.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(data={'message': 'Category Deleted!'}, status=status.HTTP_200_OK)



class DishesAPIView(APIView):
    permission_classes = [VipUser]

    def get(self, request):
        dishes = Dishes.objects.all()
        data = DishesSerializer(instance=dishes, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    #  в постмане http://127.0.0.1:8000/dishes/

    def post(self, request):
        new_dishes = DishesSerializer(data=request.data)
        if new_dishes.is_valid():
            new_dishes.save()
            return Response(data={'message': 'Dish Created!'}, status=status.HTTP_200_OK)
        else:
            return Response(data=new_dishes.errors, status=status.HTTP_400_BAD_REQUEST)

    #  в постмане http://127.0.0.1:8000/dishes/

    def patch(self, request):
        dishes = Dishes.objects.get(pk=request.data.get('id'))
        updated_dishes = DishesSerializer(dishes, data=request.data, partial=True)
        if updated_dishes.is_valid():
            updated_dishes.save()
            return Response(updated_dishes.data, status=status.HTTP_200_OK)
        return Response(data=updated_dishes.errors, status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request):
        dishes = Dishes.objects.get(pk=request.data.get('id'))
        dishes.delete()
        return Response(data={'message': 'Dishes Deleted!'}, status=status.HTTP_200_OK)


class SearchDishesApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        word = request.GET.get('search')
        if word is None:
            return Response(data={'message': 'Parameter "search" is required!'}, status=status.HTTP_400_BAD_REQUEST)
        dishes = Dishes.objects.filter(name__icontains=word)
        data = DishesSerializer(instance=dishes, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
        # в постмане http://127.0.0.1:8000/search_dishes/?search=burger

class NewDishesApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        sorting = request.GET.get('sorting')
        if sorting is None:
            dishes = Dishes.objects.all()
        else:
            if sorting == 'price-asc':
                dishes = Dishes.objects.all().order_by('charge') # по возрастанию цены

            elif sorting == 'price-desc':
                dishes = Dishes.objects.all().order_by('-charge')  # по убыванию цены

            elif sorting == 'name-asc':
                dishes = Dishes.objects.all().order_by('name')  # по алфавиту
            elif sorting == 'name-desc':
                dishes = Dishes.objects.all().order_by('-name')  # по алфавиту в обратном порядке
                # в постмане http://127.0.0.1:8000/new_dishes/?sorting=name-asc

        data = DishesSerializer(instance=dishes, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)


import requests



class RandomRecipeApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        response = requests.get('https://www.themealdb.com/api/json/v1/1/random.php')
        randomrecipe_data = response.json()
        data = {
            'name': randomrecipe_data['meals'][0]['strMeal'],
            'instructions': randomrecipe_data['meals'][0]['strInstructions']
        }
        return Response(data=data, status=status.HTTP_200_OK)
        #  в постмане http://127.0.0.1:8000/random-recipe/


class AuthApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        from django.contrib.auth import authenticate, login

        email = request.data.get('email')
        if email is None:
            return Response(data={'message': 'Field "email" is required!'}, status=status.HTTP_400_BAD_REQUEST)
        password = request.data.get('password')
        if password is None:
            return Response(data={'message': 'Field "password" is required!'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)
        if user is None:
            return Response(data={'message': 'Email and/or Password is not valid!'}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        return Response(data={'message': 'Welcome'}, status=status.HTTP_200_OK)



class RegistrationApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if email is None:
            return Response(data={'message': 'Email is required!'}, status=status.HTTP_400_BAD_REQUEST)

        password = request.data.get('password')
        if password is None:
            return Response(data={'message': 'Password is required!'}, status=status.HTTP_400_BAD_REQUEST)

        password1 = request.data.get('password1')
        if password1 is None:
            return Response(data={'message': 'Password1 is required!'}, status=status.HTTP_400_BAD_REQUEST)

        if password != password1:
            return Response(data={'message': 'Password and Password1 not match!'}, status=status.HTTP_400_BAD_REQUEST)

        CustomUser.objects.create_user(email=email, password=password)
        return Response(data={'message': 'User Created!'}, status=status.HTTP_200_OK)

class UserCabinetApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.user)

        data = CustomUserSerializer(instance=request.user, many=False).data
        print(data)
        return Response(data=data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = CustomUserSerializer(instance=request.user, data=request.data, partial=True)
        if user.is_valid():
            user.save()
            return Response(data=user.data, status=status.HTTP_200_OK)
        return Response(data=user.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        request.user.delete()
        return Response(data={"message":" User Delete"})


from rest_framework.pagination import PageNumberPagination
class DishesPaginatedApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        all_dishes = Dishes.objects.all()

        paginator = PageNumberPagination()

        dishes = paginator.paginate_queryset(all_dishes, request)

        data = DishesSerializer(instance=dishes, many=True).data

        return Response(data=data, status=status.HTTP_200_OK)

# postman http://127.0.0.1:8000/paginator?page=1

from rest_framework import serializers


from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'is_dish']


class DishesSerializer(serializers.ModelSerializer):


    class Meta:

        model = Dishes
        fields = ['id', 'name', 'price', 'description', 'rating', 'category']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance=instance.category).data
        return representation





class DrinksSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance=instance.category).data
        return representation

    class Meta:
        model = Drinks
        fields = ['id', 'name', 'price', 'description', 'rating', 'category']


class DeliverySerializer(serializers.ModelSerializer):

    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Delivery
        fields = ['id', 'dishes', 'drinks', 'delivery_date', 'delivery_address', 'total_price']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["dishes"] = DishesSerializer(instance=instance.dishes.all(),many = True).data
        representation["drinks"] = DrinksSerializer(instance=instance.drinks.all(), many=True).data
        return representation



class RecipeSerializer(serializers.Serializer):
    name = serializers.CharField()
    instructions = serializers.CharField()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'age', 'number']

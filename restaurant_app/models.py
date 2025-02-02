from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    is_dish = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Dishes(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    category = models.ForeignKey('Category', related_name='dishes', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Drinks(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    category = models.ForeignKey('Category', related_name='drinks', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Delivery(models.Model):
    dishes = models.ManyToManyField('Dishes')
    drinks = models.ManyToManyField('Drinks')
    delivery_date = models.DateTimeField()
    delivery_address = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_total_price(self):


        total_price = sum(dish.price for dish in self.dishes.all()) + sum(drink.price for drink in self.drinks.all())
        self.total_price = total_price
        self.save()

    def __str__(self):
        return f"Delivery on {self.delivery_date} to {self.delivery_address} with total price {self.total_price}"


class RandomRecipe(models.Model):
    name = models.CharField(max_length=255)
    instructions = models.TextField()

    def __str__(self):
        return self.name


from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    number = models.CharField(max_length=20, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
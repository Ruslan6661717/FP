from django.contrib import admin
from .models import *

admin.site.register(Dishes)
admin.site.register(Category)
admin.site.register(Drinks)
admin.site.register(Delivery)
admin.site.register(RandomRecipe)
admin.site.register(CustomUser)


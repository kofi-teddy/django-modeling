from django.contrib import admin
from .models import Pizza, Topping, ToppingAmount

admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(ToppingAmount)

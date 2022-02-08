from django.contrib import admin
from .models import Car, Rate, Manufacturer

# Register your models here.
admin.site.register((Car, Rate, Manufacturer))

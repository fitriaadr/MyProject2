from django.contrib import admin
from .models import Vegetable, VegetablePrice, PlantingGuide, CareGuide

admin.site.register(Vegetable)
admin.site.register(VegetablePrice)
admin.site.register(PlantingGuide)
admin.site.register(CareGuide)
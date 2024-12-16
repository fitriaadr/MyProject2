from django.contrib import admin
from .models import Vegetable, VegetablePrice, PlantingGuide, CareGuide


@admin.register(Vegetable)
class VegetableAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(VegetablePrice)
class VegetablePriceAdmin(admin.ModelAdmin):
    list_display = ('vegetable', 'price_per_kg', 'updated_at')
    search_fields = ('vegetable__name',)


@admin.register(PlantingGuide)
class PlantingGuideAdmin(admin.ModelAdmin):
    list_display = ('vegetable',)
    search_fields = ('vegetable__name',)


@admin.register(CareGuide)
class CareGuideAdmin(admin.ModelAdmin):
    list_display = ('vegetable',)
    search_fields = ('vegetable__name',)

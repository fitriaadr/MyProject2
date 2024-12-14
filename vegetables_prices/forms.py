from django import forms
from .models import VegetablePrice

class VegetablePriceForm(forms.ModelForm):
    class Meta:
        model = VegetablePrice
        fields = ['vegetable', 'price_per_kg']
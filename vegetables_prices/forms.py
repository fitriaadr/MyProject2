from django import forms
from .models import Vegetable, VegetablePrice, VegetableSeedCalculator

class VegetableForm(forms.ModelForm):
    class Meta:
        model = Vegetable
        fields = ['name', 'image', 'description']


class VegetablePriceForm(forms.ModelForm):
    class Meta:
        model = VegetablePrice
        fields = ['vegetable', 'price_per_kg']

class VegetableSeedCalculatorForm(forms.ModelForm):
    class Meta:
        model = VegetableSeedCalculator
        fields = ['vegetable', 'seeds_per_plant', 'plant_spacing_cm', 'yield_per_plant']

class PlantingCalculatorForm(forms.Form):
    vegetable = forms.ChoiceField(
        choices=[],
        label="Pilih Sayuran",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    area_size = forms.DecimalField(
        label="Luas Lahan (m²)",
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan luas lahan dalam m²'})
    )
    planting_distance = forms.DecimalField(
        label="Jarak Tanam (cm)",
        max_digits=5,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan jarak tanam dalam cm'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set choices secara dinamis dari model Vegetable
        self.fields['vegetable'].choices = [
            (vegetable.id, vegetable.name) for vegetable in Vegetable.objects.all()
        ]

    # Validasi untuk luas lahan
    def clean_area_size(self):
        area_size = self.cleaned_data.get('area_size')
        if area_size is None or area_size <= 0:
            raise forms.ValidationError("Luas lahan harus lebih besar dari 0.")
        return area_size

    # Validasi untuk jarak tanam
    def clean_planting_distance(self):
        planting_distance = self.cleaned_data.get('planting_distance')
        if planting_distance is None or planting_distance <= 0:
            raise forms.ValidationError("Jarak tanam harus lebih besar dari 0.")
        return planting_distance

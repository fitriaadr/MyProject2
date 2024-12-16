from django.db import models


class Vegetable(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='vegetables/')
    description = models.TextField()

    def __str__(self):
        return self.name


class VegetablePrice(models.Model):
    vegetable = models.ForeignKey(Vegetable, on_delete=models.CASCADE)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.vegetable.name} - {self.price_per_kg} per kg'


class VegetableSeedCalculator(models.Model):
    vegetable = models.ForeignKey(Vegetable, on_delete=models.CASCADE)
    seeds_per_plant = models.DecimalField(max_digits=10, decimal_places=2)
    yield_per_plant = models.DecimalField(max_digits=10, decimal_places=2)
    plant_spacing_cm = models.DecimalField(max_digits=10, decimal_places=2)
    row_spacing_cm = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.vegetable.name} - Kalkulasi Bibit"

class PlantingGuide(models.Model):
    vegetable = models.OneToOneField(Vegetable, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Panduan Menanam {self.vegetable.name}"

class CareGuide(models.Model):
    vegetable = models.OneToOneField(Vegetable, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Panduan Perawatan {self.vegetable.name}"

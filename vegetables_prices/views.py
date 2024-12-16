from django.views.generic import CreateView, UpdateView, ListView, DetailView
from .models import Vegetable, VegetablePrice, PlantingGuide, CareGuide
from .forms import VegetableForm, VegetablePriceForm, PlantingCalculatorForm
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

class VegetableCreateView(CreateView):
    model = Vegetable
    form_class = VegetableForm
    template_name = 'vegetables_prices/vegetable_form.html'
    success_url = reverse_lazy('vegetable_list')

class VegetableUpdateView(UpdateView):
    model = Vegetable
    form_class = VegetableForm
    template_name = 'vegetables_prices/vegetable_form.html'
    success_url = reverse_lazy('vegetable_list')

class VegetableListView(ListView):
    model = Vegetable
    template_name = 'vegetables_prices/vegetable_list.html'
    context_object_name = 'vegetables'

class VegetableDetailView(DetailView):
    model = Vegetable
    template_name = 'vegetables_prices/vegetable_detail.html'
    context_object_name = 'vegetable'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vegetables'] = Vegetable.objects.all()
        vegetable = context['vegetable']
        price = VegetablePrice.objects.filter(vegetable=vegetable).first()
        context['price'] = price
        return context

class VegetablePriceCreateView(CreateView):
    model = VegetablePrice
    form_class = VegetablePriceForm
    template_name = 'vegetables_prices/vegetable_price_form.html'
    success_url = reverse_lazy('vegetable_list')

def calculate_seed(request, vegetable_id):
    vegetable = get_object_or_404(Vegetable, id=vegetable_id)

    if request.method == 'POST':
        form = PlantingCalculatorForm(request.POST)
        if form.is_valid():
            area_size = form.cleaned_data['area_size']
            planting_distance = form.cleaned_data['planting_distance']

            if area_size <= 0 or planting_distance <= 0:
                return render(request, 'vegetables_prices/seeds_calculator.html', {
                    'form': form,
                    'vegetable': vegetable,
                    'error_message': 'Luas lahan dan jarak tanam harus lebih dari 0.',
                })

            planting_distance_m = planting_distance / 100  # cm to meter
            seeds_per_m2 = 1 / (planting_distance_m ** 2)
            total_seeds = int(seeds_per_m2 * area_size)

            # Redirect ke halaman hasil
            return render(request, 'vegetables_prices/seed_calculator_result.html', {
                'vegetable': vegetable,
                'total_seeds': total_seeds,
                'area_size': area_size,
                'planting_distance': planting_distance,
            })
    else:
        form = PlantingCalculatorForm()

    return render(request, 'vegetables_prices/seeds_calculator.html', {
        'form': form,
        'vegetable': vegetable,
    })

@login_required
def planting_guide(request, vegetable_id):
    vegetable = get_object_or_404(Vegetable, id=vegetable_id)
    guide = PlantingGuide.objects.filter(vegetable=vegetable).first()

    return render(request, 'vegetables_prices/planting_guide.html', {
        'vegetable': vegetable,
        'planting_guide': guide
    })


@login_required
def care_guide(request, vegetable_id):
    vegetable = get_object_or_404(Vegetable, id=vegetable_id)

    guide = CareGuide.objects.filter(vegetable=vegetable).first()

    return render(request, 'vegetables_prices/care_guide.html', {
        'vegetable': vegetable,
        'care_guide': guide
    })
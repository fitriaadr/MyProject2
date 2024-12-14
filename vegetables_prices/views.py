from django.shortcuts import render, get_object_or_404, redirect
from .models import Vegetable, VegetablePrice, PlantingGuide, CareGuide
from django.contrib import messages
from .forms import VegetablePriceForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage, PageNotAnInteger
import os

def vegetable_detail(request, vegetable_id):
    vegetable = get_object_or_404(Vegetable, id=vegetable_id)
    planting = PlantingGuide.objects.filter(vegetable=vegetable).first()
    care = CareGuide.objects.filter(vegetable=vegetable).first()

    return render(request, 'vegetables_prices/vegetable_detail.html', {
        'vegetable': vegetable,
        'planting_guide': planting,
        'care_guide': care,
    })

@login_required
def vegetable_guide(request):
    from django.conf import settings
    print("Base directory:", settings.BASE_DIR)
    print("Looking for template at:",
          os.path.join(settings.BASE_DIR, 'vegetables_prices/templates/vegetables_prices/vegetable_guide.html'))

    vegetables = Vegetable.objects.all()
    return render(request, 'vegetables_prices/vegetable_guide.html', {'vegetables': vegetables})

@login_required
def list_prices(request):
    query = request.GET.get('q')
    if query:
        prices_list = VegetablePrice.objects.filter(vegetable__name__icontains=query)
    else:
        prices_list = VegetablePrice.objects.all()

    paginator = Paginator(prices_list, 10)  # 10 items per page
    page_number = request.GET.get('page')
    try:
        prices = paginator.get_page(page_number)
    except PageNotAnInteger:
        prices = paginator.page(1)
    except EmptyPage:
        prices = paginator.page(paginator.num_pages)

    return render(request, 'vegetables_prices/list.html', {'prices': prices})

@login_required
def create_price(request):
    if request.method == 'POST':
        form = VegetablePriceForm(request.POST)
        if form.is_valid():
            # Validasi duplikasi (opsional)
            if VegetablePrice.objects.filter(
                vegetable=form.cleaned_data['vegetable'],
                price=form.cleaned_data['price']
            ).exists():
                messages.error(request, 'Harga untuk sayur ini sudah ada.')
            else:
                form.save()
                messages.success(request, 'Harga berhasil ditambahkan!')
                return redirect('list_prices')
        else:
            messages.error(request, 'Terdapat kesalahan dalam formulir. Mohon periksa kembali.')
    else:
        form = VegetablePriceForm()

    return render(request, 'vegetables_prices/create.html', {'form': form})

@login_required
def delete_price(request, price_id):
    if request.method == 'POST':
        price = get_object_or_404(VegetablePrice, id=price_id)
        price.delete()
        messages.success(request, 'Harga berhasil dihapus!')
    else:
        messages.error(request, 'Hapus harga hanya diperbolehkan melalui metode POST.')
    return redirect('list_prices')

@login_required
def vegetable_detail(request, vegetable_id):
    vegetable = get_object_or_404(Vegetable, id=vegetable_id)
    return render(request, 'vegetables_prices/vegetable_detail.html', {'vegetable': vegetable})

@login_required
def planting_guide(request, vegetable_id):
    vegetable = get_object_or_404(Vegetable, id=vegetable_id)
    return render(request, 'vegetables_prices/planting_guide.html', {'vegetable': vegetable})

@login_required
def care_guide(request, vegetable_id):
    vegetable = get_object_or_404(Vegetable, id=vegetable_id)
    return render(request, 'vegetables_prices/care_guide.html', {'vegetable': vegetable})

@login_required
def calculate_seeds(request, vegetable_id):
    vegetable = get_object_or_404(Vegetable, id=vegetable_id)

    if request.method == 'POST':
        area = request.POST.get('area')
        if not area or not area.isdigit():
            messages.error(request, 'Input area tidak valid. Harap masukkan angka positif.')
        else:
            area = float(area)
            if area <= 0:
                messages.error(request, 'Luas area harus lebih dari 0!')
            else:
                spacing = {'bayam': 0.5, 'cabai': 0.6, 'daun_bawang': 0.15}.get(vegetable.name.lower(), 0)
                if spacing == 0:
                    messages.error(request, 'Jarak tanam untuk sayur ini tidak tersedia.')
                else:
                    seeds = (area / spacing) ** 2
                    return render(request, 'vegetables_prices/seeds_result.html', {
                        'vegetable': vegetable,
                        'seeds': int(seeds)
                    })

    return render(request, 'vegetables_prices/seeds_calculator.html', {'vegetable': vegetable})

@login_required
def price_list(request, vegetable_id):
    vegetable = get_object_or_404(Vegetable, id=vegetable_id)
    prices = VegetablePrice.objects.filter(vegetable=vegetable).select_related('vegetable').order_by('-updated_at')

    return render(request, 'vegetables_prices/price_list.html', {'vegetable': vegetable, 'prices': prices})

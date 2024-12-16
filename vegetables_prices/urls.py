from django.urls import path
from . import views

urlpatterns = [
    path('', views.VegetableListView.as_view(), name='vegetable_list'),
    path('create/', views.VegetableCreateView.as_view(), name='vegetable_create'),
    path('<int:pk>/update/', views.VegetableUpdateView.as_view(), name='vegetable_update'),
    path('<int:pk>/', views.VegetableDetailView.as_view(), name='vegetable_detail'),

    # Price & Seed Calculator
    path('<int:pk>/price/create/', views.VegetablePriceCreateView.as_view(), name='vegetable_price_create'),

    # Planting and Care Guides
    path('<int:vegetable_id>/planting-guide/', views.planting_guide, name='planting_guide'),
    path('<int:vegetable_id>/care-guide/', views.care_guide, name='care_guide'),
    path('<int:vegetable_id>/calculate-seeds/', views.calculate_seed, name='calculate_seeds'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('vegetable-detail/<int:vegetable_id>/', views.vegetable_detail, name='vegetable_detail'),
    path('planting-guide/<int:vegetable_id>/', views.planting_guide, name='planting_guide'),
    path('care-guide/<int:vegetable_id>/', views.care_guide, name='care_guide'),
    path('calculate-seeds/<int:vegetable_id>/', views.calculate_seeds, name='calculate_seeds'),
    path('price-list/<int:vegetable_id>/', views.price_list, name='price_list'),
    path('<int:vegetable_id>/', views.vegetable_detail, name='vegetable_detail'),
]

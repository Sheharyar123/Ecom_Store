from django.urls import path
from .views import (HomePageView, 
    ItemDetailView, 
    add_to_cart, 
    add_single_to_cart,
    remove_from_cart, 
    remove_single_from_cart,
    OrderSummaryView,
    CheckoutView,
)

app_name = 'base'

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('order_summary/', OrderSummaryView.as_view(), name='order_summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('<slug:slug>/', ItemDetailView.as_view(), name='product'),
    path('add_to_cart/<slug:slug>/', add_to_cart, name='add_to_cart'),
    path('add_single_to_cart/<slug:slug>/', add_single_to_cart, name='add_single_to_cart'),
    path('remove_from_cart/<slug:slug>/', remove_from_cart, name='remove_from_cart'),
    path('remove_single_from_cart/<slug:slug>/', remove_single_from_cart, name='remove_single_from_cart'),
]

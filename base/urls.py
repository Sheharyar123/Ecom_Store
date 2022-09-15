from django.urls import path
from .views import HomePageView, ItemDetailView, add_to_cart, remove_from_cart

app_name = 'base'

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('<slug:slug>/', ItemDetailView.as_view(), name='item_detail'),
    path('add_to_cart/<slug:slug>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug:slug>/', remove_from_cart, name='remove_from_cart'),
]

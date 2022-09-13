from django.urls import path
from .views import HomePageView, ItemDetailView

app_name = 'base'

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('<slug:slug>/', ItemDetailView.as_view(), name='item_detail'),
]

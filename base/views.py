from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
# from django.contrib import messages
from .models import Item

# Create your views here.
class HomePageView(ListView):
    model = Item
    context_object_name = 'item_list'
    template_name = 'base/index.html'
    paginate_by = 12

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('q')
        if query is None:
            return Item.objects.all()
        return Item.objects.filter(
            Q(category__icontains=query) | Q(title__icontains=query)
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = Item.objects.values('category').annotate(Count('id'))
        return context


class ItemDetailView(DetailView):
    model = Item
    template_name = 'base/item_detail.html'
    context_object_name = 'item'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['related_products'] = Item.objects.filter(
         Q(price=self.object.price) | Q(category=self.object.category) 
        ).exclude(id=self.object.id).order_by('-updated_on', 'added_on')[:4]
        return context
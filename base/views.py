from django.views.generic import ListView
from django.db.models import Q
from .models import Item

# Create your views here.
class HomePageView(ListView):
    model = Item
    context_object_name = 'item_list'
    template_name = 'base/index.html'

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('q')
        if query is None:
            return Item.objects.all()
        return Item.objects.filter(
            Q(category__icontains=query) | Q(title__icontains=query)
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = Item.objects.all()
        return context
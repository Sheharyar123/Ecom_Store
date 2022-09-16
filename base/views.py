from email.mime import message
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View, TemplateView
from django.db.models import Q, Count
from django.contrib import messages
from .models import Item, OrderItem, Order

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


class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item
    template_name = 'base/product.html'
    context_object_name = 'item'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['related_products'] = Item.objects.filter(
         Q(price=self.object.price) | Q(category=self.object.category) 
        ).exclude(id=self.object.id).order_by('-updated_on', 'added_on')[:4]
        return context


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'base/checkout.html'



class OrderSummaryView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.filter(user=self.request.user, ordered=False)[0]
            order_items = order.items.all()
            context = {
                'order_items': order_items,
                'order': order,
            }
            return render(self.request, 'base/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("base:index")
            
        

@login_required
def add_to_cart(request, slug):
    '''
    Takes an item, create an order item and add
    it in the order if it doesn't exist
    or updates the order item if it exists
    '''
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Check if order item is in the order
        if order.items.filter(item__slug=slug).exists():
            order_item.quantity += int(request.POST.get("quantity"))
            order_item.save()
            messages.info(request, "Your cart was updated")
            return redirect(item.get_absolute_url())
        else:
            order.items.add(order_item)
            order_item.quantity += int(request.POST.get("quantity"))
            order_item.save()
            messages.info(request, "This item was added to your cart.")
            return redirect(item.get_absolute_url())
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user,
            ordered_date=ordered_date,
        )
        order.items.add(order_item)
        quantity = int(request.POST.get("quantity"))
        if quantity >= 1:
            order_item.quantity += int(request.POST.get("quantity"))
            order_item.save()
            messages.info(request, "This item was added to your cart.")
            return redirect(item.get_absolute_url())
        else:
            messages.info(request, "Your cart can't be empty.")
            return redirect(item.get_absolute_url())

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=slug).exists():
            order_item = OrderItem.objects.filter(
                user=request.user, 
                item=item,
                ordered=False,
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was deleted from your cart")
            return redirect('base:order_summary')
        else:
            messages.info(request, "Your cart does not have this order item")
            return redirect('base:order_summary')
    else:
        messages.info(request, "You don't have an order yet")
        return redirect('base:order_summary')

@login_required
def add_single_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.filter(
        user=request.user,
        item=item,
        ordered=False,
    )[0]
    order_item.quantity += 1
    order_item.save()
    return redirect('base:order_summary')

@login_required
def remove_single_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order = Order.objects.filter(user=request.user, ordered=False)[0]
    order_item = OrderItem.objects.filter(
        user=request.user, 
        item=item,
        ordered=False,
    )[0]
    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
        return redirect('base:order_summary')
    else:
        order.items.remove(order_item)
        order_item.delete()
        messages.info(request, "This item was deleted from your cart")
        return redirect('base:order_summary')







        


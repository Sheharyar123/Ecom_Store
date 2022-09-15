from django.contrib import admin
from .models import Item, Order, OrderItem

# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'price', 'discount_price', 'stock', 'added_on')

admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem)
admin.site.register(Order)
from django.contrib import admin
from .models import Item

# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'price', 'discount_price', 'stock', 'added_on')

admin.site.register(Item, ItemAdmin)
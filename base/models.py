from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.conf import settings

# Create your models here.
class Item(models.Model):
    ITEM_LABEL = (
        ('danger', 'New'),
        ('primary', 'Sale'),
    )

    ITEM_CATEGORY = (
        ('shirt', 'Shirt'),
        ('sportwear', 'Sport wear'),
        ('outwear', 'Outwear'),
    )

    title = models.CharField(max_length=50, unique=True)
    label = models.CharField(choices=ITEM_LABEL, max_length=10, null=True, blank=True)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    discount_price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    category = models.CharField(choices=ITEM_CATEGORY, max_length=10)
    image = models.ImageField(upload_to='clothing_pics', null=True, blank=True)
    description = models.TextField()
    stock = models.IntegerField(default=1)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_on', '-added_on']


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Item, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("base:item_detail", kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse("base:add_to_cart", kwargs={"slug": self.slug})

    def get_remove_from_cart_url(self):
        return reverse("base:remove_from_cart", kwargs={"slug": self.slug})
    

    # @property
    # def imageurl(self): 
    #     if self.image:
    #         return self.image.url
    #     return '/static/img/placeholder.jpg'


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orderitems',
                            null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='orderitems')
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.quantity:
            return f"{self.quantity} of {self.item.title}"

    class Meta:
        ordering = ['-added_on']

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Order"

    def get_total(self):
        orderitems = self.items.all()
        total = sum([item.get_final_price() for item in orderitems])
        return total


    

   


    

    
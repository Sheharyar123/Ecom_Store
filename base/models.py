from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Item(models.Model):
    ITEM_LABEL = (
        ('new', 'danger'),
        ('bestseller', 'primary'),
        ('sale', 'warning'),
    )

    ITEM_CATEGORY = (
        ('S', 'Shrit'),
        ('SW', 'Sport wears'),
        ('OW', 'Outwears'),
    )

    title = models.CharField(max_length=50, unique=True)
    label = models.CharField(choices=ITEM_LABEL, max_length=10)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    discount_price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    category = models.CharField(choices=ITEM_CATEGORY, max_length=2)
    image = models.ImageField(upload_to='clothing_pics')
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

    # def get_absolute_url():


    

    
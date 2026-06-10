from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models
from cloudinary.models import CloudinaryField
# Create your models here.
class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_friendly_name(self):
        return self.friendly_name

class Product(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    isbn = models.CharField(max_length=13)
    title = models.CharField(max_length=254)
    author = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    featured_image = CloudinaryField('image', default='placeholder')

    def __str__(self):
        return self.title

class Order(models.Model):

    """A record of a completed Stripe payment."""

    STATUS_CHOICES = [

        ('pending',   'Pending'),

        ('complete',  'Complete'),

        ('cancelled', 'Cancelled'),

    ]
 
    product           = models.ForeignKey(Product, on_delete=models.PROTECT,
                            related_name='orders')
    stripe_session_id = models.CharField(max_length=200, unique=True)
    customer_email    = models.EmailField()
    amount_paid       = models.PositiveIntegerField(help_text="Amount in pence")
    currency          = models.CharField(max_length=3, default='GBP')
    status            = models.CharField(max_length=10, choices=STATUS_CHOICES,
                            default='pending')
    shipping_address_name      = models.CharField(max_length=100, default='')
    shipping_address_line1     = models.CharField(max_length=200, default='')
    shipping_address_line2      = models.CharField(max_length=200, default='')
    shipping_address_city     = models.CharField(max_length=200, default='')
    shipping_address_postcode  = models.CharField(max_length=20, default='')
    shipping_address_country   = models.CharField(max_length=100, default='')

    billing_address_name      = models.CharField(max_length=100, default='')
    billing_address_line1     = models.CharField(max_length=200, default='')
    billing_address_line2      = models.CharField(max_length=200, default='')
    billing_address_city     = models.CharField(max_length=200, default='')
    billing_address_postcode  = models.CharField(max_length=20, default='')
    billing_address_country   = models.CharField(max_length=100, default='')
    created_at        = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"Order #{self.pk} — {self.product.title} ({self.status})"
 
    @property

    def amount_display(self):

        return f"£{self.amount_paid / 100:.2f}"
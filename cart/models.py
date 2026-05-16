from django.db import models

# Create your models here.
from users.models import User
from products.models import ProductVariant

class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} Cart"
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="items")
    product_variant = models.ForeignKey(ProductVariant,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("cart","product_variant")

    def __str__(self):
        return(f"{self.product_variant.product.name}" f" - {self.quantity}")
        
    @property
    def subtotal(self):
        return self.product_variant_price * self.quantity
        




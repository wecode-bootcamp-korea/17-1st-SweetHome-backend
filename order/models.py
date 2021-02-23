from django.db import models

from user.models    import User
from product.models import ProductOption

class Order(models.Model):
    user                   = models.ForeignKey('user.User', on_delete=models.CASCADE)
    status                 = models.ForeignKey('OrderStatus', on_delete=models.CASCADE)
    created_at             = models.DateTimeField(auto_now_add=True)
    sender_name            = models.CharField(max_length=45, null=True)
    sender_email           = models.CharField(max_length=45, null=True)
    sender_phone_number    = models.CharField(max_length=45, null=True)
    recipient_name         = models.CharField(max_length=45, null=True)
    recipient_phone_number = models.CharField(max_length=45, null=True)
    recipient_address      = models.CharField(max_length=255, null=True)
    total_price            = models.DecimalField(decimal_places=2, max_digits=12, null=True)

    class Meta:
        db_table = 'orders'

class OrderStatus(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'order_statuses'

class OrderProduct(models.Model):
    product_option = models.ForeignKey('product.ProductOption', on_delete=models.SET_NULL, null=True)
    quantity       = models.IntegerField()
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)
    order          = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'order_products'
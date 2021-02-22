from django.db import models

from user.models    import User
from product.models import ProductOption

class Order(models.Model):
    created_at             = models.DateTimeField(auto_now_add=True)
    sender_name            = models.CharField(max_length=45)
    sender_email           = models.CharField(max_length=45)
    sender_phone_number    = models.CharField(max_length=45)
    recipient_name         = models.CharField(max_length=45)
    recipient_phone_number = models.CharField(max_length=45)
    recipient_address      = models.CharField(max_length=255)
    total_price            = models.DecimalField(decimal_places=2, max_digits=12)

    class Meta:
        db_table = 'orders'

class OrderStatus(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'order_statuses'

class OrderProduct(models.Model):
    user           = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    product_option = models.ForeignKey('product.ProductOption', on_delete=models.SET_NULL, null=True)
    quantity       = models.IntegerField()
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)
    status         = models.ForeignKey('OrderStatus', on_delete=models.SET_NULL, null=True)
    order          = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'order_products'
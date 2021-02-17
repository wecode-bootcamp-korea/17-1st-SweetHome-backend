from django.db import models

from user.models    import User
from product.models import ProductOption

class Recipient(models.Model):
    name         = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=45)
    address      = models.CharField(max_length=255)

    class Meta:
        db_table = 'recipients'

class Order(models.Model):
    user                = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    recipient           = models.ForeignKey('Recipient', on_delete=models.SET_NULL, null=True)
    sender_name         = models.CharField(max_length=45)
    sender_email        = models.CharField(max_length=45)
    sender_phone_number = models.CharField(max_length=45)
    total_amount        = models.DecimalField(decimal_places=2, max_digits=12)

    class Meta:
        db_table= 'orders'

class OrderProduct(models.Model):
    product_option = models.ForeignKey('product.ProductOption', on_delete=models.SET_NULL, null=True)
    quantity       = models.IntegerField()
    order          = models.ForeignKey('Order', on_delete=models.CASCADE)

    class Meta:
        db_table = 'order_products'

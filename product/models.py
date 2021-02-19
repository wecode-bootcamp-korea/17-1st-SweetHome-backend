from django.db import models

from user.models import User

class Category(models.Model):
    name = models.CharField(max_length=45, unique=True)

    class Meta:
        db_table = 'categories'

class SubCategory(models.Model):
    name     = models.CharField(max_length=45)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_categories'

class DetailCategory(models.Model):
    name         = models.CharField(max_length=45)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE)

    class Meta:
        db_table = 'detail_categories'

class Product(models.Model):
    detail_category     = models.ForeignKey('DetailCategory', on_delete=models.CASCADE)
    name                = models.CharField(max_length=45, unique=True)
    original_price      = models.DecimalField(decimal_places=2, max_digits=12)
    discount_percentage = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    company             = models.ForeignKey('ProductCompany', on_delete=models.CASCADE)
    delivery            = models.ForeignKey('ProductDelivery', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products'

class ProductImage(models.Model):
    image_url = models.URLField(max_length=2000)
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_images'

class ProductCompany(models.Model):
    name = models.CharField(max_length=45, unique=True)

    class Meta:
        db_table = 'product_companies'

class ProductReview(models.Model):
    user       = models.ForeignKey('user.User', on_delete=models.CASCADE)
    product    = models.ForeignKey('Product', on_delete=models.CASCADE)
    content    = models.CharField(max_length=255)
    image_url  = models.URLField(max_length=2000, null=True)
    rate       = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    like_user  = models.ManyToManyField('user.User', through='ReviewLike', related_name='user_like_review')

    class Meta:
        db_table = 'product_reviews'

class ReviewLike(models.Model):
    user   = models.ForeignKey('user.User', on_delete=models.CASCADE)
    review = models.ForeignKey('ProductReview', on_delete=models.CASCADE)

    class Meta:
        db_table = 'review_likes'

class ProductOption(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    size    = models.ForeignKey('ProductSize', on_delete=models.CASCADE)
    color   = models.ForeignKey('ProductColor', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_options'

class ProductSize(models.Model):
    name = models.CharField(max_length=45, unique=True)

    class Meta:
        db_table = 'product_sizes'

class ProductColor(models.Model):
    name = models.CharField(max_length=45, unique=True)

    class Meta:
        db_table = 'product_colors'

class ProductDelivery(models.Model):
    period = models.ForeignKey('DeliveryPeriod', on_delete=models.CASCADE)
    fee    = models.ForeignKey('DeliveryFee', on_delete=models.CASCADE, null=True)
    method = models.ForeignKey('DeliveryType', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_deliveries'

class DeliveryPeriod(models.Model):
    day = models.IntegerField(unique=True)

    class Meta:
        db_table = 'delivery_periods'

class DeliveryFee(models.Model):
    price = models.IntegerField(unique=True)

    class Meta:
        db_table = 'delivery_fees'

class DeliveryType(models.Model):
    name = models.CharField(max_length=45, unique=True)

    class Meta:
        db_table = 'delivery_types'

from django.urls import path, include

urlpatterns = [
    path('orders', include('order.urls')),
    path('products', include('product.urls')),
    path('posting', include('posting.urls')),
    path('user', include('user.urls')),
]

from django.urls import path, include

urlpatterns = [
    path('products', include('product.urls'))
]
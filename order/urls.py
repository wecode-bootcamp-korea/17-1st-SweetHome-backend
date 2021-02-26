from django.urls   import path

from order.views import OrderProductView

urlpatterns = [
    path('/products', OrderProductView.as_view()),
]

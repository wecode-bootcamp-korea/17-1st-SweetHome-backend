from django.urls import path

from .views import ProductView, ProductReviewView, ProductCartView

urlpatterns = [
    path('', ProductView.as_view()),
    path('/cart', ProductCartView.as_view()),
    path('/<int:product_id>/review', ProductReviewView.as_view()),
]

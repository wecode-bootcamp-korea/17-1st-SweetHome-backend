from django.urls import path

from .views import ProductView, ProductDetailView, ProductReviewView

urlpatterns = [
    path('', ProductView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/<int:product_id>/review', ProductReviewView.as_view()),
]

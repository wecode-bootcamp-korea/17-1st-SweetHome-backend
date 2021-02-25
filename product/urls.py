from django.urls import path

from .views import ProductView, ProductDetailView, ProductReviewView, ReviewLikeView

urlpatterns = [
    path('', ProductView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/<int:product_id>/review', ProductReviewView.as_view()),
    path('/<int:product_id>/review-like', ReviewLikeView.as_view()),
]

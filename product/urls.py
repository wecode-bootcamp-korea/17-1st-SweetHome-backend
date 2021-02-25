from django.urls import path

from .views import ProductView, ProductReviewView, ReviewLikeView

urlpatterns = [
    path('', ProductView.as_view()),
    path('/<int:product_id>/review', ProductReviewView.as_view()),
    path('/<int:product_id>/review-like', ReviewLikeView.as_view()),
]

from django.urls   import path

from product.views import (
     ProductReviewView, ReviewLikeView
)

urlpatterns = [
    path('/<int:product_id>/review', ProductReviewView.as_view()),
    path('/<int:product_id>/review-like', ReviewLikeView.as_view()),
]

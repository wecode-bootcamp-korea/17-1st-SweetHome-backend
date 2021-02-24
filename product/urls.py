from django.urls   import path

from product.views import (
    ProductReviewView
)

urlpatterns = [
    path('/<int:product_id>/review', ProductReviewView.as_view()),
]

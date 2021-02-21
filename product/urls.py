from django.urls import path
from .views import ProductView

urlpatterns = [
    path('', ProductView.as_view()),
]

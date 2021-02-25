from django.urls import path
from .views      import PostingScrapView


urlpatterns = [
    path('/scrap', PostingScrapView.as_view()),
]
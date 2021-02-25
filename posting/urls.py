from django.urls import path

from posting.views  import PostingView, CategoryView

urlpatterns = [
    path('', PostingView.as_view()),
    path('/category', CategoryView.as_view()),
    path('/scrap', PostingScrapView.as_view())
]

from django.urls import path

from posting.views  import PostingView, CategoryView, PostingLikeView

urlpatterns = [
    path('', PostingView.as_view()),
    path('/category', CategoryView.as_view()),
    path('/like', PostingLikeView.as_view())
]

from django.urls import path
from .views      import SignupView
from .views      import SigninView

urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/signin', SigninView.as_view())
]
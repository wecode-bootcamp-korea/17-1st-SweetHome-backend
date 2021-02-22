from django.urls import path, include

urlpatterns = [
    path('posting', include('posting.urls')),
]

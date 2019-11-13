from django.urls import path
from .views import FeedBackCreateView

urlpatterns = [
    path('add', FeedBackCreateView.as_view(), name='feedback-create')
]

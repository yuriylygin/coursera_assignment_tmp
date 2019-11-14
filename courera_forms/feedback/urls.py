from django.urls import path
from .views import FeedBackCreateView, FeedbackListView

urlpatterns = [
    path('add', FeedBackCreateView.as_view(), name='feedback-create'),
    path('', FeedbackListView.as_view(), name='feedback-list')
]

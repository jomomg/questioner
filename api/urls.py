from django.urls import path
from api import views

urlpatterns = [
    path('events', views.EventList.as_view(), name='event-list'),
    path('events/<str:pk>', views.EventDetail.as_view(), name='event-detail'),
    path('questions', views.QuestionList.as_view(), name='question-list'),
    path('questions/<str:pk>', views.QuestionDetail.as_view(), name='question-detail'),
]

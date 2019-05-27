from django.urls import path
from api.views import event, question

urlpatterns = [
    path('events', event.EventList.as_view(), name='event-list'),
    path('events/<str:pk>', event.EventDetail.as_view(), name='event-detail'),
    path('questions', question.QuestionList.as_view(), name='question-list'),
    path('questions/<str:pk>', question.QuestionDetail.as_view(), name='question-detail')
]

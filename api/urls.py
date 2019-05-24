from django.urls import path
from api import views

urlpatterns = [
    path('events', views.EventList.as_view(), name='event-list'),
    path('events/<str:event_id>', views.EventDetail.as_view(), name='event-detail')
]

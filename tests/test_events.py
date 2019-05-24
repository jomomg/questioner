import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Event

EVENT_DATA = {
    'title': 'Comic Con',
    'location': 'Nairobi',
    'happening_on': datetime.date(2019, 6, 7)
}


class EventTests(APITestCase):
    def test_creating_an_event_succeeds(self):
        url = reverse('event-list')
        response = self.client.post(url, EVENT_DATA, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['data']['title'], EVENT_DATA['title'])
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.get().title, EVENT_DATA['title'])

    def test_getting_all_events_succeeds(self):
        url = reverse('event-list')
        for i in range(3):
            self.client.post(url, EVENT_DATA, format='json')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 3)

    def test_getting_single_event_succeeds(self):
        url = reverse('event-list')
        res = self.client.post(url, EVENT_DATA, format='json')
        event_id = res.data['data']['id']
        url = reverse('event-detail', kwargs={'event_id': event_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['id'], event_id)

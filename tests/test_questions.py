from django.urls import reverse
from rest_framework import status

from .utils import AuthenticatedBaseTestCase
from api.models import Question, Event
from .fixtures import EVENT_DATA, QUESTION_DATA


class EventTests(AuthenticatedBaseTestCase):
    @staticmethod
    def create_event():
        event = Event(**EVENT_DATA)
        event.save()
        return event

    def create_question_data_with_event_id(self):
        event = self.create_event()
        question_data = QUESTION_DATA.copy()
        question_data['event'] = event.id
        return question_data

    def test_creating_a_question_succeeds(self):
        question_data = self.create_question_data_with_event_id()
        url = reverse('question-list')
        response = self.client.post(url, question_data, format='json')
        res_data = response.data['data']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(res_data['title'], question_data['title'])
        self.assertEqual(res_data['event'], question_data['event'])
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Question.objects.get().title, question_data['title'])

    def test_getting_all_questions_succeeds(self):
        url = reverse('question-list')
        event = self.create_event()
        for i in range(3):
            question = Question(event=event, **QUESTION_DATA)
            question.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 3)

    def test_getting_single_question_succeeds(self):
        question_data = self.create_question_data_with_event_id()
        url = reverse('question-list')
        res = self.client.post(url, question_data, format='json')
        question_id = res.data['data']['id']
        url = reverse('question-detail', kwargs={'pk': question_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['id'], question_id)

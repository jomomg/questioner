import datetime

from django.test import TestCase

from api.models import Event, Question, Image

EVENT_DATA = {
    'location': 'Nairobi',
    'title': 'AWS',
    'happening_on': datetime.date(2019, 6, 5)
}

QUESTION_DATA = {
    'title': 'how stuff works',
    'body': 'what is this thing',
    'votes': -32
}


class EventModelTests(TestCase):
    def test_saving_an_event_succeeds(self):
        event = Event(**EVENT_DATA)
        event.save()
        now = datetime.datetime.utcnow()
        all_events = Event.objects.all()
        self.assertEqual(all_events.count(), 1)
        saved_event = Event.objects.get(title=EVENT_DATA['title'])
        self.assertEqual(
            (now.minute, now.second),
            (saved_event.created_at.minute, saved_event.created_at.second))


class QuestionModelTests(TestCase):
    def test_saving_question_succeeds(self):
        event = Event(**EVENT_DATA)
        event.save()
        question_data = QUESTION_DATA.copy()
        question_data['event'] = event
        question = Question(**question_data)
        question.save()
        now = datetime.datetime.utcnow()
        all_questions = Question.objects.all()
        self.assertEqual(all_questions.count(), 1)
        saved_question = Question.objects.get(title=QUESTION_DATA['title'])
        self.assertEqual(
            (now.minute, now.second),
            (saved_question.created_at.minute, saved_question.created_at.second))


class ImageModelTests(TestCase):
    def test_saving_image_succeeds(self):
        event = Event(**EVENT_DATA)
        event.save()
        image_data = {'url': 'sample_url', 'event': event}
        image = Image(**image_data)
        image.save()
        all_images = Image.objects.all()
        self.assertEqual(all_images.count(), 1)

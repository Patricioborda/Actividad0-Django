import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question(self):
        Question.objects.create(
            question_text="Pregunta futura.",
            pub_date=timezone.now() + datetime.timedelta(days=30)
        )
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        question = Question.objects.create(
            question_text="Pregunta pasada.",
            pub_date=timezone.now() - datetime.timedelta(days=1)
        )
        response = self.client.get(reverse("polls:index"))
        # Comparar solo el texto de las preguntas
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [question.question_text],  # Solo comparamos el texto de la pregunta
            transform=str
        )

    def test_future_and_past_question(self):
        past_question = Question.objects.create(
            question_text="Pasada",
            pub_date=timezone.now() - datetime.timedelta(days=1)
        )
        future_question = Question.objects.create(
            question_text="Futura",
            pub_date=timezone.now() + datetime.timedelta(days=1)
        )
        response = self.client.get(reverse("polls:index"))
        # Comparar solo el texto de la pregunta pasada
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question.question_text],  # Solo comparamos el texto de la pregunta pasada
            transform=str
        )

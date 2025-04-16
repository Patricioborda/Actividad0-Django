import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question, Choice

# ✅ Función auxiliar
def create_question(question_text, days):
    """
    Crea una pregunta con `question_text` y pub_date con offset `days` respecto a ahora.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

# 🧪 Tests del modelo
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

# 🧪 Tests de IndexView
class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        question = create_question("Past question.", days=-1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question])

    def test_future_question(self):
        create_question("Future question.", days=1)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_and_past_question(self):
        past_question = create_question("Past question.", days=-1)
        create_question("Future question.", days=1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [past_question])

    def test_two_past_questions(self):
        question1 = create_question("Past question 1.", days=-30)
        question2 = create_question("Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question2, question1])

    def test_question_without_choices_not_shown(self):
        """
        Tests that questions without any choices are not shown in the index view.
        """
        question = create_question("Pregunta sin opciones", days=-1)
        # No le agregamos choices
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

# 🧪 Tests de DetailView
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question("Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question("Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

# 🧪 Tests de ResultsView
class ResultsViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question("Future question.", days=3)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question("Past question.", days=-3)
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)

# 🧪 Tests de votación
class VoteViewTests(TestCase):
    def test_vote_valid_choice(self):
        question = create_question("¿Pizza o empanadas?", days=-1)
        choice = Choice.objects.create(question=question, choice_text="Pizza", votes=0)
        response = self.client.post(
            reverse("polls:vote", args=(question.id,)),
            {"choice": choice.id}
        )
        self.assertRedirects(response, reverse("polls:results", args=(question.id,)))
        choice.refresh_from_db()
        self.assertEqual(choice.votes, 1)

    def test_vote_no_choice_selected(self):
        question = create_question("¿Verano o invierno?", days=-1)
        Choice.objects.create(question=question, choice_text="Verano", votes=0)
        response = self.client.post(
            reverse("polls:vote", args=(question.id,)),
            {}  # sin enviar 'choice'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You didn't select a choice.")

    def test_vote_on_future_question(self):
        future_question = create_question("¿2025 será mejor?", days=5)
        choice = Choice.objects.create(question=future_question, choice_text="Sí", votes=0)
        url = reverse("polls:vote", args=(future_question.id,))
        response = self.client.post(url, {"choice": choice.id})
        self.assertEqual(response.status_code, 404)

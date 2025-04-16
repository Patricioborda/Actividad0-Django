from django.urls import path
from . import views

app_name = "polls"  # Define el espacio de nombres para las URLs de esta app

urlpatterns = [
    # ex: /polls/
    path("", views.IndexView.as_view(), name="index"),  # Usa IndexView (ListView)
    # ex: /polls/5/
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),  # Usa DetailView
    # ex: /polls/5/results/
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),  # Usa ResultsView (también DetailView)
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),  # Vista de voto sigue siendo una función
]

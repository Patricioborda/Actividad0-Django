# polls/admin.py
from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Question

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date')
    list_filter = ('pub_date',)
    search_fields = ('question_text',)

    def save_model(self, request, obj, form, change):
        """
        Sobrescribe el método save_model para evitar que se publiquen preguntas sin opciones.
        """
        if obj.choice_set.count() == 0:
            raise ValidationError("No puedes guardar una pregunta sin opciones.")
        super().save_model(request, obj, form, change)

# Registrar el modelo con el admin personalizado
admin.site.register(Question, QuestionAdmin)

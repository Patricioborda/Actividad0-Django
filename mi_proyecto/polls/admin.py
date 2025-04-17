# polls/admin.py
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

    def clean(self):
        super().clean()
        if not any(form.cleaned_data and not form.cleaned_data.get("DELETE", False) for form in self.forms):
            raise ValidationError("Debe agregar al menos una opción.")

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date')
    list_filter = ('pub_date',)
    search_fields = ('question_text',)

    def save_model(self, request, obj, form, change):
        if obj.choice_set.count() == 0:
            raise ValidationError("No puedes guardar una pregunta sin opciones.")
        super().save_model(request, obj, form, change)

admin.site.register(Question, QuestionAdmin)

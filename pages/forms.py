from django import forms
from django.conf import settings
from django.utils.translation import get_language

class LanguageForm(forms.Form):
    language = forms.ChoiceField(
        choices=settings.LANGUAGES,
        initial=get_language,
        widget=forms.Select(attrs={'onchange': 'this.form.submit()'})
    )
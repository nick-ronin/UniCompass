from .forms import LanguageForm
from django.utils import translation

def language_form(request):
    return {
        'language_form': LanguageForm(initial={'language': translation.get_language()}),
        'current_language': translation.get_language(),
    }
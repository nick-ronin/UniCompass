from django.shortcuts import render, redirect
from django.utils import translation
from django.conf import settings

def set_language(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        if language:
            translation.activate(language)
            response = redirect(request.META.get('HTTP_REFERER', 'home'))
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
            return response
    return redirect('home')

def home(request):
    template_name = 'en/home.html' if translation.get_language() == 'en' else 'pages/home.html'
    return render(request, template_name)


def calendar(request):
    days = list(range(1, 32))  # дни октября
    current_language = translation.get_language()

    if current_language == 'en':
        template_name = 'en/calendar.html'
    else:
        template_name = 'pages/calendar.html'

    return render(request, template_name, {'days': days})

def tasks(request):
    template_name = 'en/tasks.html' if translation.get_language() == 'en' else 'pages/tasks.html'
    return render(request, template_name)

def knowledge_base(request):
    template_name = 'en/knowledge_base.html' if translation.get_language() == 'en' else 'pages/knowledge_base.html'
    return render(request, template_name)

def contacts(request):
    template_name = 'en/contacts.html' if translation.get_language() == 'en' else 'pages/contacts.html'
    return render(request, template_name)

def mfc_detail(request):
    template_name = 'en/mfc_detail.html' if translation.get_language() == 'en' else 'pages/mfc_detail.html'
    return render(request, template_name)
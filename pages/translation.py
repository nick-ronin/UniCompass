TRANSLATIONS = {
    'ru': {
        'Calendar': 'Календарь',
        'Tasks': 'Список заданий',
        'Home': 'Главная',
        'Knowledge Base': 'База знаний',
        'Contacts': 'Контакты',
        'Welcome to main page!': 'Добро пожаловать на главную страницу!',
        'This is our first page.': 'Это наша первая страница.',
        'Here will be calendar': 'Здесь будет календарь',
        'Here will be tasks': 'Здесь будут задания',
        'Here will be knowledge base': 'Здесь будет база знаний',
        'Here will be contacts': 'Здесь будут контакты',
    },
    'en': {
        'Calendar': 'Calendar',
        'Tasks': 'Tasks',
        'Home': 'Home',
        'Knowledge Base': 'Knowledge Base',
        'Contacts': 'Contacts',
        'Welcome to main page!': 'Welcome to main page!',
        'This is our first page.': 'This is our first page.',
        'Here will be calendar': 'Here will be calendar',
        'Here will be tasks': 'Here will be tasks',
        'Here will be knowledge base': 'Here will be knowledge base',
        'Here will be contacts': 'Here will be contacts',
    }
}

def get_translation(text, language):
    return TRANSLATIONS.get(language, {}).get(text, text)
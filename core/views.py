from django.shortcuts import render

def main_page(request):
    # Determine which template to use based on user role
    if request.user.is_authenticated and getattr(request.user, 'is_admin', False):
        template_name = 'core/main_page_admin.html'
    else:
        template_name = 'core/main_page.html'
    
    return render(request, template_name, {"show_search": True})
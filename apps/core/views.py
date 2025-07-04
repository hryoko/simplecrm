from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView


# @login_required
class HomeView(TemplateView):
    template_name = 'core/home.html'


# def index(request):
#     return render(request, 'core/index.html')

# def dashboard(request):
#     return render(request, 'core/dashboard.html')


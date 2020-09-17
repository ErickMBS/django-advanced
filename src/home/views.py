from django.views.generic import TemplateView
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views import View


def calcular(v1, v2):
    return v1 / v2


def home(request):
    value1 = 10
    value2 = 20
    res = calcular(value1, value2)
    return render(request, 'home/home.html', {'result': res})


def my_logout(request):
    logout(request)
    return redirect('home')


class HomePageView(TemplateView):
    template_name = 'home3.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['minha_variavel'] = 'Ola, seja bem vindo ao curso de Django advanced'
        return context


class MyView(View):

    def get(self, request, *args, **kwargs):
        response = render_to_response('home3.html')
        response.set_cookie('color', 'blue', max_age=1000)
        my_cookie = request.COOKIES.get('color')
        print(my_cookie)
        return response

    def post(self, request, *args, **kwargs):
        return HttpResponse('Post!')

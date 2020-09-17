from .views import home, my_logout, HomePageView, MyView
from django.views.generic.base import TemplateView
from django.urls import path


urlpatterns = [
    path('', home, name="home"),
    path('logout/', my_logout, name="logout"),
    path('home2/', TemplateView.as_view(template_name='home2.html')),
    path('home3/', HomePageView.as_view(),),
    path('hello/', MyView.as_view())
]

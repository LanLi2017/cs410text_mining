from django.urls import path
from django.views.generic.base import RedirectView

from subscribe import views

app_name = 'subscribe'
urlpatterns = [
    path('', RedirectView.as_view(url='./register')),
    path('register', views.register, name='register'),
    path('<str:token>/subscribe', views.subscribe, name='subscribe'),
]

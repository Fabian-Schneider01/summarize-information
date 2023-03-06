from django.urls import path

from . import views

app_name = 'summarize_information'

urlpatterns = [
    path('', views.index, name='index'),
]
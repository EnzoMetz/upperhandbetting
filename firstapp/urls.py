from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from firstapp import views

app_name = 'firstapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('resources/', views.resources, name='resources'),
    path('formpage/', views.form_name_view, name='formpage')
]
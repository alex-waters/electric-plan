from django.urls import path
from . import views

urlpatterns = [
    path('', views.page_list, name='page_list'),
]
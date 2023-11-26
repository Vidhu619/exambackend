from django.urls import path
from .views import QuestionsList
from . import views
urlpatterns = [
     path('questions', QuestionsList, name='questions-list'),
    path('register', views.Register,name='register'),
    path('login', views.Login, name='login'),
     path('categories', views.category_list, name='category-list'),
]
from django.urls import path
from .views import *
from . import views
urlpatterns = [
    path('questions', Question_list, name='questions-list'),
    path('register', views.Register,name='register'),
    path('login', views.Login, name='login'),
     path('categories', views.category_list, name='category-list'),
     path('queston_list',views.Question) ,
]
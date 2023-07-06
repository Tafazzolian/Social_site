from django.urls import path
from . import views

app_name = 'base'
urlpatterns = [
    path('welcome/',views.welcome, name='welcome'),
    path('',views.HomePage.as_view(), name='home'),

]
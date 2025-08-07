from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name='home'),
    path('build/', views.build, name='build'),


    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
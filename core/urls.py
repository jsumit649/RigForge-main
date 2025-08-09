from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name='home'),
    path('build/', views.PCBuildpage, name='build'),


    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('cart/', views.cart, name='cart'),
]
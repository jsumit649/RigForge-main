from . import views
from . import api_views
from django.urls import path


urlpatterns = [
    path('', views.home, name='home'),
    path('build/', views.PCBuildpage, name='build'),


    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('cart/', views.cart, name='cart'),

    path('components/', views.componentspage, name='components'),

    path('api/cpus/', api_views.cpu_list, name='api-cpus'),
    path('api/gpus/', api_views.gpu_list, name='api-gpus'),
    path('api/motherboards/', api_views.motherboard_list, name='api-motherboards'),
    path('api/ram/', api_views.ram_list, name='api-ram'),
    path('api/hddstorage/', api_views.hdd_storage_list, name='api-hdd-storage'),
    path('api/ssdstorage/', api_views.ssd_storage_list, name='api-ssd-storage'),
    path('api/power-supplies/', api_views.psu_list, name='api-power-supplies'),
    path('api/cases/', api_views.case_list, name='api-cases'),
    path('api/coolers/', api_views.cpu_cooler_list, name='api-coolers'),
    path('api/add-to-cart/', api_views.add_to_cart, name='api-add-to-cart'),
]
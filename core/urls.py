from . import api_views
from django.urls import path
from .views import (
    HomeView, LoginPageView, LogoutUserView, RegisterPageView, EditProfileView,
    CartView, ComponentsPageView, PCBuildPageView, RemoveBuildView, RemoveFromCartView,
    EditBuildView, DeleteAddressView, CheckoutView
)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('build/', PCBuildPageView.as_view(), name='build'),


    path('login/', LoginPageView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('register/', RegisterPageView.as_view(), name='register'),
    path('profile/', EditProfileView.as_view(), name='profile'),

    path('cart/', CartView.as_view(), name='cart'),

    path('components/', ComponentsPageView.as_view(), name='components'),

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

    path('cart/remove-build/<int:build_id>/', RemoveBuildView.as_view(), name='remove-build'),
    path('cart/remove-item/<int:item_id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('build/edit/<int:build_id>/', EditBuildView.as_view(), name='edit-build'),

    path('address/delete/<int:address_id>/', DeleteAddressView.as_view(), name='delete-address'),

    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
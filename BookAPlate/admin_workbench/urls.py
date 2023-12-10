from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView, CustomerListView, CustomerStatus, CustomerDetailsView, RestaurantListView, RestaurantStatus, RestaurantDetailsView,LogoutView,ChangePasswordView

urlpatterns=[
    path('',HomeView,name='admin_home'),
    path('customer_list/',CustomerListView,name='customer_list'),
    path('customer_status/',CustomerStatus,name='customer_status'),
    path('customer_details/',CustomerDetailsView,name='customer_details'),
    path('restaurant_list/',RestaurantListView,name='restaurant_list'),
    path('restaurant_status/',RestaurantStatus,name='restaurant_status'),
    path('restaurant_details/',RestaurantDetailsView,name='restaurant_details'),
    path('change_password/',ChangePasswordView,name='change_password'),
    path('logout/',LogoutView,name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
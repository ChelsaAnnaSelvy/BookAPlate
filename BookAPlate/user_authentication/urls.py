from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from .views import LoginView,HomeView,SuccessView,CustomerRegistrationView,RestaurantRegistrationView

urlpatterns = [    
    
    path('',HomeView,name='home'),
    path('login/',LoginView,name='login'),
    path('customer_registration/',CustomerRegistrationView,name='customer'),
    path('restaurant_Registration/',RestaurantRegistrationView,name='restaurant'),
    path('success/',SuccessView,name='success'),
    path('customer_user/',include('customer.urls')),
    path('restaurant_user/',include('restaurant.urls')),
    path('admin_user/',include('admin_workbench.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
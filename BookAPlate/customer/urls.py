from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from customer.views import HomeView, CustomerProfileView, RestaurantListView,RestaurantProfileView,TableView,BookTableView

urlpatterns=[
    path('',HomeView,name='customer_home'),
    path('profile/',CustomerProfileView,name='customer_profile'),
    path('restaurants/',RestaurantListView,name='restaurants'),
    path('restaurant_profile/',RestaurantProfileView,name='restaurant_profile'),
    path('view_table/',TableView,name='view_table'),
    path('book_table/',BookTableView,name='book_table'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
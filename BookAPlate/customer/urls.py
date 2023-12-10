from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView, CustomerProfileView, RestaurantListView, RestaurantProfileView, TableView, ConfirmBookTableView, BookTable,BookingHistoryView,BookingDetailsView,LogoutView,CancelBooking,ChangePasswordView
urlpatterns=[
    path('',HomeView,name='customer_home'),
    path('profile/',CustomerProfileView,name='customer_profile'),
    path('restaurants/',RestaurantListView,name='restaurants'),
    path('restaurant_profile/',RestaurantProfileView,name='restaurant_profile'),
    path('view_table/',TableView,name='view_table'),
    path('confirm_book_table/',ConfirmBookTableView,name='confirm_booking_table'),
    path('book_table/',BookTable,name='book_table'),
    path('reservations/',BookingHistoryView,name='my_reservations'),
    path('booking_details/',BookingDetailsView,name='booking_details'),
    path('cancel_booking/',CancelBooking,name='cancel_booking'),
    path('logout/',LogoutView,name='logout'),
    path('customer_change_password/',ChangePasswordView,name='customer_change_password'),
    
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
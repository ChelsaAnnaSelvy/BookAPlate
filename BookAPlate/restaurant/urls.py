from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    HomeView, ProfileDetailsView, GalleryDetailsView,
    DeleteGalleryItem, EditGalleryItem, FacilityDetailsView,
    DeleteFacilityItem, EditFacilityItem, LogoutView,
    BookingDetailsView, ReceiptView, MarkAsAttendedView, ChangePasswordView
)

urlpatterns = [
    path('', HomeView, name='restaurant_home'),
    path('profile_details', ProfileDetailsView, name='profile_details'),
    path('gallery_details/', GalleryDetailsView, name='gallery_details'),
    path('delete_gallery_item/', DeleteGalleryItem, name='delete_gallery_item'),
    path('edit_gallery_item/', EditGalleryItem, name='edit_gallery_item'),
    path('facility_details/', FacilityDetailsView, name='facility_details'),
    path('delete_facility_item/', DeleteFacilityItem, name='delete_facility_item'),
    path('edit_facility_item/', EditFacilityItem, name='edit_facility_item'),
    path('reservations/', BookingDetailsView, name='reservations'),
    path('logout/', LogoutView, name='logout'), 
    path('booking_receipt/', ReceiptView, name='receipt'),
    path('attended/', MarkAsAttendedView, name='mark_as_attended'),
    path('restaurant_change_password/', ChangePasswordView, name='restaurant_change_password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

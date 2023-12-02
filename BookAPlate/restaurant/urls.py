from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from restaurant.views import HomeView, GalleryDetailsView, DeleteGalleryItem, EditGalleryItem, FacilityDetailsView, DeleteFacilityItem,EditFacilityItem

urlpatterns=[
    path('',HomeView,name='restaurant_home'),
    path('gallery_details/',GalleryDetailsView,name='gallery_details'),
    path('delete_gallery_item/',DeleteGalleryItem,name='delete_gallery_item'),
    path('edit_gallery_item/',EditGalleryItem,name='edit_gallery_item'),
    path('facility_details/',FacilityDetailsView,name='facility_details'),
    path('delete_facility_item/',DeleteFacilityItem,name='delete_facility_item'),
    path('edit_facility_item/',EditFacilityItem,name='edit_facility_item'),
   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
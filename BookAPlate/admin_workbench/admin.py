from django.contrib import admin
from .models import Customer, Restaurant, BookingDetails, FacilityDetails, Gallery, Coins

# Register your models here.

class FacilityDetailsInline(admin.TabularInline):
    model = FacilityDetails
    extra = 1

class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 1

class BookingDetailsInline(admin.TabularInline):
    model = BookingDetails
    extra = 1

class CustomerAdmin(admin.ModelAdmin):
    inlines = [BookingDetailsInline]
    list_display = ('customer_id', 'phone', 'address', 'place', 'state', 'status')
    search_fields = ['phone']

class RestaurantAdmin(admin.ModelAdmin):
    inlines = [FacilityDetailsInline, GalleryInline]
    list_display = ('restaurant_id', 'phone', 'address', 'place', 'state', 'status')
    search_fields = ['phone']

class FacilityDetailsAdmin(admin.ModelAdmin):
    list_display = ('facility_id', 'facility_name', 'facility_number', 'seat_count', 'seat_arrangement', 'restaurant')
    search_fields = ['facility_number']

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('gallery_id', 'title', 'category', 'restaurant')
    search_fields = ['title']

class BookingDetailsAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'date', 'status', 'meal_time', 'customer')
    search_fields = ['booking_id']



class CoinsAdmin(admin.ModelAdmin):
    list_display = ('coin_id', 'coin_quantity', 'user')
    search_fields = ['coin_id']

# Register the models with the admin site
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(FacilityDetails, FacilityDetailsAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(BookingDetails, BookingDetailsAdmin)
admin.site.register(Coins, CoinsAdmin)

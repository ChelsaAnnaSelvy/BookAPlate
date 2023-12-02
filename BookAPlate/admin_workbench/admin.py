from django.contrib import admin
from .models import Customer, Restaurant, BookingDetails, FacilityDetails, Gallery, Feedback, Coins

# Register your models here.

# Register the CustomerProfile model with the admin site
admin.site.register(Customer)

# Register the RestaurantProfile model with the admin site
admin.site.register(Restaurant)

# Register the BookingDetails model with the admin site
admin.site.register(BookingDetails)

# Register the FacilityDetails model with the admin site
admin.site.register(FacilityDetails)

# Register the Gallery model with the admin site
admin.site.register(Gallery)


# Register the Feedback model with the admin site
admin.site.register(Feedback)

# Register the Coins model with the admin site
admin.site.register(Coins)

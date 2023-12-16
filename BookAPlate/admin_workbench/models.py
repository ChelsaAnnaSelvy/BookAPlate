from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Define your models here

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=13, unique=True)
    address = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
 
    # Define state choices as a list of tuples
    STATES_CHOICES = [
    ('','Select State'),
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal')
]
    state = models.CharField(max_length=100, choices=STATES_CHOICES,default='Kerala')
    status = models.CharField(max_length=10, default='Active')
    profile_photo = models.ImageField(upload_to='profile_pictures/', null=True)
    id_proof = models.ImageField(upload_to='customer_identifier/', null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)  

class Restaurant(models.Model):
    restaurant_id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=13, unique=True)
    address = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    # Define state choices as a list of tuples
    STATES_CHOICES = [
    ('','Select State'),
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal')
]
    state = models.CharField(max_length=100, choices=STATES_CHOICES, default='Kerala')
    status = models.CharField(max_length=10, default='Inactive')
    profile_photo = models.ImageField(upload_to='restaurant_profile/', null=True)
    pancard = models.ImageField(upload_to='business_pan/', null=True)
    description = models.TextField()
    fssai_registration_number = models.DecimalField(max_digits=14, unique=True, decimal_places=0)
    license_number = models.CharField(max_length=100, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Gallery(models.Model):
    gallery_id = models.AutoField(primary_key=True)
    photo = models.ImageField(upload_to='restaurant_gallery/', null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    # Define category choices as a list of tuples
    CATEGORY_CHOICES = [
        ('','Select Category'),
        ('Menu', 'Menu'),
        ('Gallery', 'Gallery')
    ]
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Gallery')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class FacilityDetails(models.Model):
    facility_id = models.AutoField(primary_key=True)
    facility_name = models.CharField(max_length=100,default='Table')
    facility_number =models.CharField(max_length=10)
    seat_count = models.IntegerField(default=2)     
    SEATING_LOCATION_CHOICES = [
        ('Indoor','Indoor'),
        ('Outdoor','Outdoor'),
       
    ]
    seat_arrangement =  models.CharField(max_length=100, choices=SEATING_LOCATION_CHOICES, default= 'Indoor',null=True) 
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)  

class BookingDetails(models.Model):
    booking_id = models.AutoField(primary_key=True) 
    date = models.DateField(null=True)
    STATUS_CHOICES = [
        ('Booked', 'Booked'),
        ('Completed', 'Completed'), 
        ('Cancelled','Cancelled') , 
        ('Attended','Attended')   
    ]
    status =models.CharField(max_length=100, choices=STATUS_CHOICES,default='Requested') 
    # Define meal choices as a list of tuples
    MEAL_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Supper', 'Supper'),
        
    ]
    meal_time = models.CharField(max_length=100, choices=MEAL_CHOICES,default='Full Day')
    coins_spend = models.IntegerField(default=0)
    facility = models.ManyToManyField(FacilityDetails, related_name='booking_facilities')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    booked_date= models.DateField(auto_now_add=True)
    def save(self, *args, **kwargs):
        # Generate a custom booking ID
        if not self.booking_id:
            last_booking = BookingDetails.objects.order_by('-booking_id').first()
            last_id = last_booking.booking_id if last_booking else 999
            self.booking_id = last_id + 1

        # Set the date and time components
        now = datetime.now()
        year_last_two_digits = str(now.year)[2:]
        month = str(now.month).zfill(2)
        day = str(now.day).zfill(2)
        hour = str(now.hour).zfill(2)

        # Concatenate the components to form the booking ID
        self.booking_id = f"1000{year_last_two_digits}{month}{now.year}{day}{hour}"

        # Call the original save method
        super().save(*args, **kwargs)
    
class Coins(models.Model):
    coin_id = models.AutoField(primary_key=True)
    coin_quantity = models.IntegerField(default= 2000)
    user = models.ForeignKey(Customer,on_delete=models.CASCADE)

class Feedback(models.Model):
    feedback_id= models.AutoField(primary_key=True)
    rating =models.DecimalField(max_digits=2,decimal_places=1,default=0.0)
    message=models.TextField()
    booking= models.ForeignKey(BookingDetails,on_delete=models.CASCADE)

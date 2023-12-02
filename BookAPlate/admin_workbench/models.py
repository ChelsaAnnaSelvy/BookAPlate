from django.db import models
from django.contrib.auth.models import User

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
    # Define facility choices as a list of tuples
    FACILITY_CHOICES = [
        ('','Select Facility'),
        ('Table', 'Table'),
        ('Banquet Hall', 'Banquet Hall'),
        ('Conference Hall', 'Conference Hall')
    ]
    facility_name = models.CharField(max_length=100, choices=FACILITY_CHOICES,default='Table')
    facility_number =models.CharField(max_length=10,unique = True)
    seat_count = models.IntegerField(default=2)     
    SEATING_LOCATION_CHOICES = [
        ('','Select Location'),
        ('Outdoor','Outdoor'),
        ('Indoor','Indoor'),
       
    ]
    seat_arrangement =  models.CharField(max_length=100, choices=SEATING_LOCATION_CHOICES, default= 'Indoor',null=True) 
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    

class BookingDetails(models.Model):
    booking_id = models.AutoField(primary_key=True)    
    
    date = models.DateField()
    STATUS_CHOICES = [
        ('Requested', 'Requested'),
        ('Completed', 'Completed'), 
        ('Cancelled','Cancelled') ,    
    ]
    status =models.CharField(max_length=100, choices=STATUS_CHOICES,default='Requested') 
    # Define meal choices as a list of tuples
    MEAL_CHOICES = [
        ('','Select Meal Time'),
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Supper', 'Supper'),
        
    ]
    meal_time = models.CharField(max_length=100, choices=MEAL_CHOICES,default='Full Day')
    facility = models.ManyToManyField(FacilityDetails)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    feedback = models.TextField()
    booking = models.ForeignKey(BookingDetails, on_delete=models.CASCADE)

class Coins(models.Model):
    coin_id = models.AutoField(primary_key=True)
    coin_quantity = models.IntegerField(default= 2000)
    user = models.ForeignKey(Customer,on_delete=models.CASCADE)


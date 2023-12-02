import json
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from admin_workbench.models import Customer,Restaurant,FacilityDetails,Feedback,Coins,BookingDetails,Gallery
from .forms import EditCustomerForm,UserForm
from django.contrib import messages
# Create your views here.
def HomeView(request):
    logged_user= request.user
    customer = get_object_or_404(Customer,user=logged_user) 
    context={
        'logged_user':logged_user,
        'customer': customer,
    }
    return render(request,'customer/home.html',context)

def CustomerProfileView(request):
    logged_user=request.user
    customer = get_object_or_404(Customer,user=logged_user) 
    
    
    if request.method=='POST':
        userform = UserForm(request.POST,instance=logged_user)       
        customerdetailsform = EditCustomerForm(request.POST, request.FILES,instance=customer)
        
        if userform.is_valid() and customerdetailsform.is_valid():
           
            user = userform.save()  # Save the user first
            customer = customerdetailsform.save()            
            messages.success(request, 'You have successfully updated your profile')
            return redirect('customer_profile')
    else:
      
        userform = UserForm(instance=logged_user)
        customerdetailsform = EditCustomerForm(instance=customer)  
       
        context={
        'logged_user':logged_user,
        'customer': customer,
        'form1': userform,
        'form2':customerdetailsform,
    }
        return render(request,'customer/profile.html',context)
    return redirect('customer_profile')

def RestaurantListView(request):
   logged_user=request.user
   customer = get_object_or_404(Customer,user=logged_user)    
   restaurants= Restaurant.objects.filter(status='Active')
   context={
       'logged_user': logged_user,
       'customer': customer,
       'restaurants': restaurants,
   }
  
   return render(request,'customer/restaurants.html',context) 

def RestaurantProfileView(request):
   logged_user=request.user
   customer = get_object_or_404(Customer,user=logged_user) 
   if request.method=='POST':
        restaurant_id= request.POST.get('restaurant_id',0)
        restaurant= get_object_or_404(Restaurant,restaurant_id=restaurant_id)
        restaurant_user = restaurant.user
        galleries = Gallery.objects.filter(restaurant=restaurant) 
        context={
       'logged_user': logged_user,
       'customer': customer,
       'restaurant': restaurant,
       'restaurant_galleries': galleries.filter(category='Gallery'),
       'menu_galleries': galleries.filter(category='Menu'),
       'restaurant_user':restaurant_user,
        }
        return render(request,'customer/restaurant_profile.html',context) 
   
def TableView(request):
    logged_user=request.user
    customer = get_object_or_404(Customer,user=logged_user) 
    
    if request.method=='POST':
        
        restaurant_id=request.POST.get('restaurant_id',0)       
        
        restaurant=get_object_or_404(Restaurant,restaurant_id=restaurant_id)
        facilities=FacilityDetails.objects.filter(restaurant=restaurant,facility_name='Table')
        date = request.POST.get('due_date',None)
        meal_time=request.POST.get('meal_time','')
        
        # Get booked facility IDs
        exclude_facility_ids = BookingDetails.objects.filter(date=date, meal_time=meal_time).values_list('facility__facility_id', flat=True)   

        # Get available facilities
        available_facilities = FacilityDetails.objects.exclude(facility_id__in=exclude_facility_ids)
        
        
        context={
        'facilities':facilities,
        'meal_time':BookingDetails.MEAL_CHOICES,
        'logged_user':logged_user,
        'customer':customer,    
        'available':available_facilities,
        'restaurant':restaurant,
        'date':date,
        'meal':meal_time,
    }        
        return render(request,'customer/view_table.html',context)
    
    context={
        'meal_time':BookingDetails.MEAL_CHOICES,
        'logged_user':logged_user,
        'customer':customer,
    }
    
    return render(request,'customer/view_table.html',context)

def BookTableView(request):
    if request.method == 'POST':
        # Retrieve the selected facilities JSON string from the form data
        selected_facilities_json = request.POST.get('selected_facilities')

        if selected_facilities_json:
            # Parse the JSON string to get a list of selected facilities
            selected_facilities = json.loads(selected_facilities_json)

            # Now 'selected_facilities' contains a list of dictionaries with 'facilityNumber' and 'seatCount' keys
            # You can process this data as needed in your views.py

            # For example, print the selected facilities
            for facility in selected_facilities:
                facility_number = facility.get('facilityNumber')
                seat_count = facility.get('seatCount')
                print(f'Selected Facility: {facility_number}, Seat Count: {seat_count}')

            # Perform your further processing here

    # Your existing code for rendering the template or any other logic
    return redirect('restaurantsThank you')
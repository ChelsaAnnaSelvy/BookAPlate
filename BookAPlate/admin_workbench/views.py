from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Customer,Restaurant
from django.contrib import messages


# Create your views here.
def HomeView(request):
    logged_user=request.user
    context={
        'logged_user': logged_user,
        'today':datetime.now()
        }
    return render(request,'admin_workbench/home.html',context)

def LogoutView(request):
    # Logout the user
    logout(request)
    
    # Redirect to homepage
    return redirect('login')  

def CustomerListView(request):

    logged_user=request.user
    
    customers= Customer.objects.all()
    active_customers=Customer.objects.filter(status='Active')
    inactive_customers= Customer.objects.filter(status='Inactive')
    context= {
        'customers': customers,
        'active_customers': active_customers,
        'inactive_customers': inactive_customers,
        'today':datetime.now(),
    }
    return render(request,'admin_workbench/customer_list.html',context)

def RestaurantListView(request):

    logged_user=request.user
    
    restaurants= Restaurant.objects.all()
    active_restaurants=Restaurant.objects.filter(status='Active')
    inactive_restaurants= Restaurant.objects.filter(status='Inactive')
    context= {
        'restaurants': restaurants,
        'active_restaurants': active_restaurants,
        'inactive_restaurants': inactive_restaurants,
        'today':datetime.now(),
    }
    return render(request,'admin_workbench/restaurant_list.html',context)

def RestaurantStatus(request):
    if request.method == 'POST':
        status = request.POST.get("status")
        restaurant_id= int(request.POST.get('restaurant_id',0))
        print(restaurant_id)
        restaurant= get_object_or_404(Restaurant,restaurant_id= restaurant_id)
        
        if status == 'Active':
            restaurant.status= 'Active'
            restaurant.save()
            # Add a success message
            messages.success(request, 'The restaurant is successfully Activated.')
            
        else:
            restaurant.status= 'Inactive'
            restaurant.save()
            # Add a success message
            messages.success(request, 'The restaurant is successfully Deactivated.')       
        
        return redirect('restaurant_list')

def RestaurantDetailsView(request):
    if request.method == 'POST':        
        restaurant_id= int(request.POST.get('restaurant_id',0))
        
        restaurant= get_object_or_404(Restaurant,restaurant_id= restaurant_id)
        
        
    return render(request,'admin_workbench/restaurant_details.html',{'restaurant':restaurant,'today':datetime.now()})

def CustomerStatus(request):
    if request.method == 'POST':
        status = request.POST.get("status")
        customer_id= int(request.POST.get('customer_id',0))
        
        customer= get_object_or_404(Customer,customer_id= customer_id)
        
        if status == 'Active':
            customer.status= 'Active'
            # Add a success message
            messages.success(request, 'The customer is successfully Activated.')                     
            
        else:
            customer.status= 'Inactive'
            # Add a success message
            messages.success(request, 'The customer is successfully Deactivated.')
        customer.save() 
        return redirect('customer_list')

def CustomerDetailsView(request):
    if request.method == 'POST':        
        customer_id= int(request.POST.get('customer_id',0))
        
        customer= get_object_or_404(Customer,customer_id= customer_id)
        
        
    return render(request,'admin_workbench/customer_details.html',{'customer':customer,'today':datetime.now()})
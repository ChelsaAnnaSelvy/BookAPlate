from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash, logout
from.forms import ChangePasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Customer,Restaurant,BookingDetails
from django.contrib import messages


# Create your views here.
@login_required
def HomeView(request):
    logged_user=request.user
    customer_count=Customer.objects.count()
    restaurant_count=Restaurant.objects.count()
    booking_count=BookingDetails.objects.count()
    all_count=User.objects.count()
    context={
        'logged_user': logged_user,
        'today':datetime.now(),
        'customer_count': customer_count,
        'diner_count':restaurant_count,
        'booking_count':booking_count,
        'all_count':all_count,
        }
    return render(request,'admin_workbench/home.html',context)

@login_required
def LogoutView(request):
    # Logout the user
    logout(request)
    request.session['logged_out'] = True
    
    # Redirect to homepage
    return redirect('login')  

@login_required
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
        'logged_user':logged_user
    }
    return render(request,'admin_workbench/customer_list.html',context)

@login_required
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
        'logged_user':logged_user,
    }
    return render(request,'admin_workbench/restaurant_list.html',context)

@login_required
def RestaurantStatus(request):
    if request.method == 'POST':
        status = request.POST.get("status")
        restaurant_id= int(request.POST.get('restaurant_id',0))
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

@login_required
def RestaurantDetailsView(request):
    logged_user=request.user
    if request.method == 'POST':        
        restaurant_id= int(request.POST.get('restaurant_id',0))        
        restaurant= get_object_or_404(Restaurant,restaurant_id= restaurant_id)      
        context={
            'restaurant':restaurant,
            'today':datetime.now(),
            'logged_user':logged_user,
            }
    return render(request,'admin_workbench/restaurant_details.html',context)

@login_required
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

@login_required
def CustomerDetailsView(request):
    logged_user=request.user
    if request.method == 'POST':        
        customer_id= int(request.POST.get('customer_id',0))
        
        customer= get_object_or_404(Customer,customer_id= customer_id)
        context={
            'customer':customer,
            'today':datetime.now(),
            'logged_user':logged_user,
            }
    return render(request,'admin_workbench/customer_details.html',context)

@login_required
def ChangePasswordView(request):
    logged_user = request.user

    if request.method == 'POST':
        form = ChangePasswordForm(logged_user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('admin_home')
        else:
            # Check for the specific error related to old password
            if 'old_password' in form.errors:
                messages.error(request, 'The old password you entered is incorrect. Please try again.')
            else:
                messages.error(request, 'Please correct the error below.')
    else:
        form = ChangePasswordForm(logged_user)

    context = {
        'form': form,
        'logged_user': logged_user
    }

    return render(request, 'admin_workbench/change_password.html', context)

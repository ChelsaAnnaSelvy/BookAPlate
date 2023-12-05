from datetime import datetime
import json
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from admin_workbench.models import Customer,Restaurant,FacilityDetails,Feedback,Coins,BookingDetails,Gallery
from .forms import EditCustomerForm,UserForm
from django.contrib import messages
# Create your views here.

# ... Import other necessary modules and models ...

# Helper function to get customer and coins
def get_customer_and_coins(request):
    logged_user = request.user
    customer = get_object_or_404(Customer, user=logged_user)
    coins = get_object_or_404(Coins, user=customer)
    return logged_user, customer, coins

# Home view
def HomeView(request):
    logged_user, customer, coins = get_customer_and_coins(request)
    context = {
        'logged_user': logged_user,
        'customer': customer,
        'coins': coins,
    }
    return render(request, 'customer/home.html', context)

# Customer profile view
def CustomerProfileView(request):
    logged_user, customer, coins = get_customer_and_coins(request)

    if request.method == 'POST':
        userform = UserForm(request.POST, instance=logged_user)
        customerdetailsform = EditCustomerForm(request.POST, request.FILES, instance=customer)

        if userform.is_valid() and customerdetailsform.is_valid():
            user = userform.save()  # Save the user first
            customer = customerdetailsform.save()
            messages.success(request, 'You have successfully updated your profile')
            return redirect('customer_profile')
    else:
        userform = UserForm(instance=logged_user)
        customerdetailsform = EditCustomerForm(instance=customer)

    context = {
        'logged_user': logged_user,
        'customer': customer,
        'form1': userform,
        'form2': customerdetailsform,
        'coins': coins,
    }
    return render(request, 'customer/profile.html', context)

# Restaurant list view
def RestaurantListView(request):
    logged_user, customer, coins = get_customer_and_coins(request)
    restaurants = Restaurant.objects.filter(status='Active')
    context = {
        'logged_user': logged_user,
        'customer': customer,
        'restaurants': restaurants,
        'coins': coins,
    }

    return render(request, 'customer/restaurants.html', context)

# Restaurant profile view
def RestaurantProfileView(request):
    logged_user, customer, coins = get_customer_and_coins(request)

    if request.method == 'POST':
        restaurant_id = request.POST.get('restaurant_id', 0)
        restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
        restaurant_user = restaurant.user
        galleries = Gallery.objects.filter(restaurant=restaurant)
        context = {
            'logged_user': logged_user,
            'customer': customer,
            'restaurant': restaurant,
            'restaurant_galleries': galleries.filter(category='Gallery'),
            'menu_galleries': galleries.filter(category='Menu'),
            'restaurant_user': restaurant_user,
            'coins': coins,
        }
        return render(request, 'customer/restaurant_profile.html', context)

# Table view
def TableView(request):
    logged_user, customer, coins = get_customer_and_coins(request)

    if request.method == 'POST':
        restaurant_id = request.POST.get('restaurant_id', 0)
        restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
        facilities = FacilityDetails.objects.filter(restaurant=restaurant, facility_name='Table')
        date = request.POST.get('due_date', None)
        meal_time = request.POST.get('meal_time', '')

        # Get booked facility IDs
        exclude_facility_ids = BookingDetails.objects.filter(date=date, meal_time=meal_time).values_list('facility__facility_id', flat=True)

        # Get available facilities
        available_facilities = FacilityDetails.objects.exclude(facility_id__in=exclude_facility_ids)

        context = {
            'facilities': facilities,
            'meal_time': BookingDetails.MEAL_CHOICES,
            'logged_user': logged_user,
            'customer': customer,
            'available': available_facilities,
            'restaurant': restaurant,
            'date': date,
            'meal': meal_time,
            'coins': coins,
        }
        return render(request, 'customer/view_table.html', context)

    context = {
        'meal_time': BookingDetails.MEAL_CHOICES,
        'logged_user': logged_user,
        'customer': customer,
        'coins': coins,
    }

    return render(request, 'customer/view_table.html', context)

# Confirm book table view
def ConfirmBookTableView(request):
    logged_user, customer, coins = get_customer_and_coins(request)

    if request.method == 'POST':
        selected_facilities_json = request.POST.get('selected_facilities', '[]')
        selected_facility_ids_json = request.POST.get('selected_facility_ids', '[]')

        selected_facilities = json.loads(selected_facilities_json)
        selected_facility_ids = json.loads(selected_facility_ids_json)

        facility_ids_list = []
        seat_counts_list = []

        for facility, facility_id in zip(selected_facilities, selected_facility_ids):
            seat_count = facility['seatCount']
            facility_ids_list.append(facility_id)
            seat_counts_list.append(seat_count)

        head_count = [int(num) for num in seat_counts_list]
        total = sum(head_count)
        facility_details_list = FacilityDetails.objects.filter(facility_id__in=facility_ids_list)
        facility_details_data = list(facility_details_list.values())
        meal = request.POST.get('meal', '')
        date = request.POST['date']
        if coins and coins.coin_quantity >= total * 10:  # Ensure coins is not None
            request.session['facility_details_data'] = facility_details_data
            request.session['coin_count'] = total * 10
            request.session['date'] = date
            request.session['meal_time'] = meal

            context = {
                'facilities': facility_details_data,
                'head_count': total,
                'coin_count': total * 10,
                'logged_user': logged_user,
                'customer': customer,
                'coins': coins,
                'meal': meal,
                'date': date,
            }

            return render(request, 'customer/booking_confirmation.html', context)

    context = {
        'facilities': [],
        'head_count': 0,
        'coin_count': 0,
        'logged_user': logged_user,
        'customer': customer,
        'coins': coins,
        'meal': meal,
        'date': date,
    }

    return render(request, 'customer/booking_confirmation.html', context)

# BookTableView
def BookTableView(request):
    logged_user, customer, coins = get_customer_and_coins(request)

    # Retrieve data from the session
    facility_details_data = request.session.get('facility_details_data', [])
    coin_count = request.session.get('coin_count', 0)
    meal_time = request.session.get('meal_time', 0)
    date = request.session.get('date')
    remaining_coins = coins.coin_quantity if coins else 0

    print(f'MYCOINS->{remaining_coins}, REQUIRED AMOUNT->{coin_count}')

    if remaining_coins >= coin_count and meal_time:
        coins.coin_quantity -= coin_count
        coins.save()

        # Create a BookingDetails object and set its fields
        booking = BookingDetails.objects.create(
            date=date,
            status='Booked',
            meal_time=meal_time,
            customer=customer,
        )

        # Get or create Facility instances and add them to the booking
        facilities = []
        for facility_data in facility_details_data:
            facility, created = FacilityDetails.objects.get_or_create(**facility_data)
            facilities.append(facility)

        # Use the set() method to add related objects for the many-to-many field
        booking.facility.set(facilities)

        # Save the booking after setting the facilities
        booking.save()

        # Clear session variables after successful processing
        request.session.pop('facility_details_data', None)
        request.session.pop('coin_count', None)
        request.session.pop('date', None)
        request.session.pop('meal_time', None)
        
        messages.success(request, 'You have successfully booked tables.Happy Dining!!!')

        # Redirect to my_reservations
        return redirect('my_reservations')
    else:
        # If the condition is not met, display an error message and redirect to restaurants
        messages.error(request, 'Sorry, you have insufficient coins. Kindly contact customer care to buy our coin pack')

        # Clear session variables
        request.session.pop('facility_details_data', None)
        request.session.pop('coin_count', None)
        request.session.pop('date', None)
        request.session.pop('meal_time', None)

        return redirect('restaurants')

# Booking history view
def BookingHistoryView(request):
    logged_user, customer, coins = get_customer_and_coins(request)
    my_booking = BookingDetails.objects.filter(customer=customer).order_by('-date')
    context = {
        'bookings': my_booking,
        'logged_user': logged_user,
        'customer': customer,
        'coins': coins,
    }
    return render(request, 'customer/booking_history.html', context)

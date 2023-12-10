import base64
import json
import qrcode
from datetime import datetime
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from admin_workbench.models import Customer,Restaurant,FacilityDetails,Coins,BookingDetails,Gallery
from .forms import EditCustomerForm,UserForm,ChangePasswordForm
from django.contrib.auth import logout,update_session_auth_hash
from django.contrib import messages
from io import BytesIO
from django.contrib.auth.decorators import login_required

# Create your views here.

# Helper function to get customer and coins
@login_required
def get_customer_and_coins(request):
    logged_user = request.user
    customer = get_object_or_404(Customer, user=logged_user)
    coins = get_object_or_404(Coins, user=customer)
    return logged_user, customer, coins

@login_required
def LogoutView(request):
    # Logout the user
    logout(request)
    request.session['logged_out'] = True
    
    # Redirect to homepage
    return redirect('login')  

# Home view
@login_required
def HomeView(request):
    logged_user, customer, coins = get_customer_and_coins(request)
    context = {
        'logged_user': logged_user,
        'customer': customer,
        'coins': coins,
    }
    return render(request, 'customer/home.html', context)

# Customer profile view
@login_required
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
@login_required
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
@login_required
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
@login_required
def TableView(request):
    logged_user, customer, coins = get_customer_and_coins(request)

    if request.method == 'POST':
        restaurant_id = request.POST.get('restaurant_id', 0)
        restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
        facilities = FacilityDetails.objects.filter(restaurant=restaurant, facility_name='Table')
        date = request.POST.get('due_date', None)
        meal_time = request.POST.get('meal_time', '')

        # Get booked facility IDs
        exclude_facility_ids = BookingDetails.objects.filter(date=date, meal_time=meal_time,status= 'Booked').values_list('facility__facility_id', flat=True)

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
@login_required
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
        if coins and coins.coin_quantity >= total * 30:  # Ensure coins is not None
            request.session['facility_details_data'] = facility_details_data
            request.session['coin_count'] = total * 30
            request.session['date'] = date
            request.session['meal_time'] = meal

            context = {
                'facilities': facility_details_data,
                'head_count': total,
                'coin_count': total * 30,
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
@login_required
def BookTable(request):
    logged_user, customer, coins = get_customer_and_coins(request)

    # Retrieve data from the session
    facility_details_data = request.session.get('facility_details_data', [])
    coin_count = request.session.get('coin_count', 0)
    meal_time = request.session.get('meal_time', 0)
    date = request.session.get('date')
    remaining_coins = coins.coin_quantity if coins else 0


    if remaining_coins >= coin_count and meal_time:
        coins.coin_quantity -= coin_count
        coins.save()

        # Create a BookingDetails object and set its fields
        booking = BookingDetails.objects.create(
            date=date,
            status='Booked',
            meal_time=meal_time,
            customer=customer,
            coins_spend= coin_count,
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
        request.session['booking_id']=booking.booking_id
        
        # Redirect to my_reservations
        return redirect('booking_details')
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
@login_required
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

# Cancel Booking view
@login_required
def CancelBooking(request):
    logged_user, customer, coins = get_customer_and_coins(request)
    if request.method== 'POST':
        booking_id = request.POST['booking_id']
        if booking_id != 0:
            booking= get_object_or_404(BookingDetails,booking_id=booking_id)
            booking.status='Cancelled'
            booking.save()
           
            rewarding_coins=int((booking.coins_spend/30) *10)
            coins=get_object_or_404(Coins,user=customer)
            coins.coin_quantity=int(coins.coin_quantity+rewarding_coins)
            coins.save()
            date=booking.date
            meal=booking.meal_time
            facilities=booking.facility.all()
            first_facility=booking.facility.first()
            restaurant=first_facility.restaurant            
            name=restaurant.user.first_name
            messages.success(request,f'Your booking for {date} in {name} for {meal} is cancelled.You have received {rewarding_coins} coins for successfully cancelling your Booking. Thank You.')
            
        return redirect('my_reservations')
 
#Helper function to generate qrcode 
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer)
    return buffer.getvalue()      

#Receipt for Booking 
@login_required
def BookingDetailsView(request):
    logged_user, customer, coins = get_customer_and_coins(request)
    if request.method== 'POST':
        booking_id = request.POST['booking_id']
        
        if booking_id != 0 :
            booking= get_object_or_404(BookingDetails,booking_id=booking_id)
            facilities=booking.facility.all()
            first_facility=booking.facility.first()
            restaurant=first_facility.restaurant
            my_facilities = " "
            for facility in facilities:
              my_facilities=my_facilities+ facility.facility_number +" "
            # Generate QR code for the booking_id
            # qr_code_data = f"Booking ID: {booking_id}"
            if booking.meal_time == 'Breakfast':
              time='8:00 AM - 12:00 PM'
            elif booking.meal_time == 'Lunch':
              time='12:00 PM - 4:00 PM'
            else:
              time='4:00 PM - 8:00 PM'
            
            qr_code_data = f"""           
                        This is a receipt
            ----------------------------------------------------                     
            BOOKING ID:       {booking_id}
            DATE OF BOOKING:  {booking.booked_date}
            ----------------------------------------------------
                        CUSTOMER DETAILS
            ----------------------------------------------------
            
            Customer's Name: {logged_user.first_name} {logged_user.last_name}
            Phone: {customer.phone}
            Email: {logged_user.email}

            ----------------------------------------------------
                        BOOKING DETAILS
            ----------------------------------------------------
            
            Date of Dining: {booking.date}
            Meal: {booking.meal_time}
            Time Allotted: {time}
            Tables Reserved: { my_facilities}
            Seats reserved: For {int(booking.coins_spend/10)} People
            
            ----------------------------------------------------
                    RESTAURANT DETAILS                
            ----------------------------------------------------
            
            Retaurant's Name: {restaurant.user.first_name}
            Email: {restaurant.user.email}
            Phone: {restaurant.phone}
            Address:  {restaurant.address},
                              {restaurant.place},
                              {restaurant.state}. 
                          
            ----------------------------------------------------
            Happy Dining!!! See You Soon...        
            ----------------------------------------------------
            
            
            
            """
            qr_code_image = generate_qr_code(qr_code_data)

            # Convert the binary data to a base64-encoded string
            qr_code_base64 = base64.b64encode(qr_code_image).decode("utf-8")
            context={
            'booking':booking,
            'logged_user': logged_user,
            'customer': customer,
            'coins': coins, 
            'facilities':facilities,  
            'head_count':int(booking.coins_spend/10), 
            'restaurant':restaurant,
            'qr_code':qr_code_base64,  
            }
            return render(request,'customer/booking_details.html',context)
    else:
        booking_id=request.session.get('booking_id',0)
        if booking_id != 0 :
            booking= get_object_or_404(BookingDetails,booking_id=booking_id)
            facilities=booking.facility.all()
            first_facility=booking.facility.first()
            restaurant=first_facility.restaurant
            my_facilities=''
            for facility in facilities:
                my_facilities=my_facilities+ facility.facility_number +" "
                
            # Generate QR code for the booking_id
            if booking.meal_time == 'Breakfast':
              time='8:00 AM - 12:00 PM'
            elif booking.meal_time == 'Lunch':
              time='12:00 PM - 4:00 PM'
            else:
              time='4:00 PM - 8:00 PM'
            qr_code_data = f"""           
                        This is a receipt
            ----------------------------------------------------                     
            BOOKING ID:       {booking_id}
            DATE OF BOOKING:  {booking.booked_date}
            ----------------------------------------------------
                        CUSTOMER DETAILS
            ----------------------------------------------------
            
            Customer's Name: {logged_user.first_name} {logged_user.last_name}
            Phone: {customer.phone}
            Email: {logged_user.email}

            ----------------------------------------------------
                        BOOKING DETAILS
            ----------------------------------------------------
            
            Date of Dining: {booking.date}
            Meal: {booking.meal_time}
            Time Allotted: {time}
            Tables Reserved: { my_facilities}
            Seats reserved: For {int(booking.coins_spend/10)} People
            
            ----------------------------------------------------
                    RESTAURANT DETAILS                
            ----------------------------------------------------
            
            Retaurant's Name: {restaurant.user.first_name}
            Email: {restaurant.user.email}
            Phone: {restaurant.phone}
            Address:  {restaurant.address},
                              {restaurant.place},
                              {restaurant.state}. 
                          
            ----------------------------------------------------
            Happy Dining!!! See You Soon...        
            ----------------------------------------------------
            """
            
            qr_code_image = generate_qr_code(qr_code_data)

            # Convert the binary data to a base64-encoded string
            qr_code_base64 = base64.b64encode(qr_code_image).decode("utf-8")

            context={
            'booking':booking,
            'logged_user': logged_user,
            'customer': customer,
            'coins': coins, 
            'facilities':facilities,  
            'head_count':int(booking.coins_spend/10), 
            'restaurant':restaurant,
            'qr_code':qr_code_base64,  
            }
            return render(request,'customer/booking_details.html',context)
        
    return render(request,'customer/booking_details.html')

# View for changing password
@login_required
def ChangePasswordView(request):
    logged_user, customer, coins = get_customer_and_coins(request)

    if request.method == 'POST':
        form = ChangePasswordForm(logged_user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('customer_home')
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
        'logged_user': logged_user,
        'customer': customer,
        'coins': coins, 
    }

    return render(request, 'customer/change_password.html', context)
            
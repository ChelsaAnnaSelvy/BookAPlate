import base64
from datetime import datetime
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash, logout
import qrcode
from .forms import ChangePasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Customer, Restaurant, BookingDetails, FacilityDetails, Gallery, Feedback
from django.contrib import messages


# Create your views here.
@login_required
def HomeView(request):
    logged_user = request.user
    customer_count = Customer.objects.count()
    restaurant_count = Restaurant.objects.count()
    booking_count = BookingDetails.objects.count()
    all_count = User.objects.count()
    context = {
        'logged_user': logged_user,
        'today': datetime.now(),
        'customer_count': customer_count,
        'diner_count': restaurant_count,
        'booking_count': booking_count,
        'all_count': all_count,
    }
    return render(request, 'admin_workbench/home.html', context)

@login_required
def LogoutView(request):
    # Logout the user
    logout(request)
    request.session['logged_out'] = True

    # Redirect to homepage
    return redirect('login')

@login_required
def CustomerListView(request):
    logged_user = request.user
    customers = Customer.objects.all()
    active_customers = Customer.objects.filter(status='Active')
    inactive_customers = Customer.objects.filter(status='Inactive')
    context = {
        'customers': customers,
        'active_customers': active_customers,
        'inactive_customers': inactive_customers,
        'today': datetime.now(),
        'logged_user': logged_user
    }
    return render(request, 'admin_workbench/customer_list.html', context)

@login_required
def RestaurantListView(request):
    logged_user = request.user
    restaurants = Restaurant.objects.all()
    active_restaurants = Restaurant.objects.filter(status='Active')
    inactive_restaurants = Restaurant.objects.filter(status='Inactive')
    context = {
        'restaurants': restaurants,
        'active_restaurants': active_restaurants,
        'inactive_restaurants': inactive_restaurants,
        'today': datetime.now(),
        'logged_user': logged_user,
    }
    return render(request, 'admin_workbench/restaurant_list.html', context)

@login_required
def RestaurantStatus(request):
    if request.method == 'POST':
        status = request.POST.get("status")
        restaurant_id = int(request.POST.get('restaurant_id', 0))
        restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
        if status == 'Active':
            restaurant.status = 'Active'
            restaurant.save()
            # Add a success message
            messages.success(request, 'The restaurant is successfully Activated.')
        else:
            restaurant.status = 'Inactive'
            restaurant.save()
            # Add a success message
            messages.success(request, 'The restaurant is successfully Deactivated.')

        return redirect('restaurant_list')

@login_required
def RestaurantDetailsView(request):
    logged_user = request.user
    if request.method == 'POST':
        restaurant_id = int(request.POST.get('restaurant_id', 0))
        restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
        context = {
            'restaurant': restaurant,
            'today': datetime.now(),
            'logged_user': logged_user,
        }
    return render(request, 'admin_workbench/restaurant_details.html', context)

@login_required
def CustomerStatus(request):
    if request.method == 'POST':
        status = request.POST.get("status")
        customer_id = int(request.POST.get('customer_id', 0))

        customer = get_object_or_404(Customer, customer_id=customer_id)

        if status == 'Active':
            customer.status = 'Active'
            # Add a success message
            messages.success(request, 'The customer is successfully Activated.')
        else:
            customer.status = 'Inactive'
            # Add a success message
            messages.success(request, 'The customer is successfully Deactivated.')
        customer.save()
        return redirect('customer_list')

@login_required
def CustomerDetailsView(request):
    logged_user = request.user
    if request.method == 'POST':
        customer_id = int(request.POST.get('customer_id', 0))
        customer = get_object_or_404(Customer, customer_id=customer_id)
        context = {
            'customer': customer,
            'today': datetime.now(),
            'logged_user': logged_user,
        }
    return render(request, 'admin_workbench/customer_details.html', context)

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

@login_required
def FacilitiesView(request):
    logged_user = request.user
    restaurant = None  # Initialize restaurant outside of the if statement

    if request.method == 'POST':
        restaurant_id = request.POST.get('restaurant_id')  # Use get to avoid KeyError if not present
        # You might want to add some validation for restaurant_id here

        # Assuming restaurant_id is a unique identifier for the restaurant
        restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id).first()

    if restaurant:
        facilities = FacilityDetails.objects.filter(restaurant=restaurant)
    else:
        facilities = FacilityDetails.objects.none()  # Return an empty queryset if no restaurant is selected

    context = {
        'logged_user': logged_user,
        'facilities': facilities,
        'restaurant': restaurant,
    }

    return render(request, 'admin_workbench/facilities.html', context)

@login_required
def GalleriesView(request):
    logged_user = request.user
    restaurant = None  # Initialize restaurant outside of the if statement

    if request.method == 'POST':
        restaurant_id = request.POST.get('restaurant_id')  # Use get to avoid KeyError if not present
        # You might want to add some validation for restaurant_id here

        # Assuming restaurant_id is a unique identifier for the restaurant
        restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id).first()

    if restaurant:
        galleries = Gallery.objects.filter(restaurant=restaurant)
    else:
        galleries = Gallery.objects.none()  # Return an empty queryset if no restaurant is selected

    context = {
        'logged_user': logged_user,
        'galleries': galleries,
        'restaurant': restaurant,
    }

    return render(request, 'admin_workbench/gallery.html', context)

@login_required
def BookingHistoryView(request):
    logged_user = request.user
    restaurant = None  # Initialize restaurant outside of the if statement

    if request.method == 'POST':
        restaurant_id = request.POST.get('restaurant_id')  # Use get to avoid KeyError if not present
        # You might want to add some validation for restaurant_id here

        # Assuming restaurant_id is a unique identifier for the restaurant
        restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id).first()

    if restaurant:
        facilities = FacilityDetails.objects.filter(restaurant=restaurant)
        bookings = BookingDetails.objects.filter(facility__restaurant=restaurant).order_by('date').distinct()
        feedbacks = Feedback.objects.filter(booking__facility__restaurant=restaurant).distinct()
    else:
        facilities = FacilityDetails.objects.none()  # Return an empty queryset if no restaurant is selected

    context = {
        'logged_user': logged_user,
        'facilities': facilities,
        'bookings': bookings,
        'restaurant': restaurant,
        'feedbacks': feedbacks,
    }

    return render(request, 'admin_workbench/bookings.html', context)

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

@login_required
def BookingReceiptView(request):
    logged_user = request.user

    if request.method == 'POST':
        booking_id = request.POST['booking_id']

        if booking_id != 0:
            booking = get_object_or_404(BookingDetails, booking_id=booking_id)
            customer = booking.customer
            facilities = booking.facility.all()
            first_facility = booking.facility.first()
            restaurant = first_facility.restaurant
            my_facilities = " "
            for facility in facilities:
                my_facilities = my_facilities + facility.facility_number + " "
            # Generate QR code for the booking_id
            # qr_code_data = f"Booking ID: {booking_id}"
            if booking.meal_time == 'Breakfast':
                time = '8:00 AM - 12:00 PM'
            elif booking.meal_time == 'Lunch':
                time = '12:00 PM - 4:00 PM'
            else:
                time = '4:00 PM - 8:00 PM'

            qr_code_data = f"""
                        This is a receipt
            ----------------------------------------------------
            BOOKING ID:       {booking_id}
            DATE OF BOOKING:  {booking.booked_date}
            ----------------------------------------------------
                        CUSTOMER DETAILS
            ----------------------------------------------------

            Customer's Name: {customer.user.first_name} {customer.user.last_name}
            Phone: {customer.phone}
            Email: {customer.user.email}

            ----------------------------------------------------
                        BOOKING DETAILS
            ----------------------------------------------------

            Date of Dining: {booking.date}
            Meal: {booking.meal_time}
            Time Allotted: {time}
            Tables Reserved: { my_facilities}
            Seats reserved: For {int(booking.coins_spend / 10)} People

            ----------------------------------------------------
                    RESTAURANT DETAILS
            ----------------------------------------------------

            Retaurant's Name: {logged_user.first_name}
            Email: {logged_user.email}
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
            context = {
                'booking': booking,
                'logged_user': logged_user,
                'customer': customer,
                'facilities': facilities,
                'head_count': int(booking.coins_spend / 10),
                'restaurant': restaurant,
                'qr_code': qr_code_base64,
            }
            return render(request, 'admin_workbench/booking_receipt.html', context)

    return render(request, 'admin_workbench/booking_receipt.html')


@login_required
def FeedbackList(request):
    logged_user = request.user
    restaurant = None  # Initialize restaurant outside of the if statement

    if request.method == 'POST':
        restaurant_id = request.POST.get('restaurant_id')  # Use get to avoid KeyError if not present
        # You might want to add some validation for restaurant_id here

        # Assuming restaurant_id is a unique identifier for the restaurant
        restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id).first()

    if restaurant:
        facilities = FacilityDetails.objects.filter(restaurant=restaurant)
        bookings = BookingDetails.objects.filter(facility__restaurant=restaurant).order_by('date').distinct()
        feedbacks = Feedback.objects.filter(booking__facility__restaurant=restaurant).distinct()
    else:
        facilities = FacilityDetails.objects.none()  # Return an empty queryset if no restaurant is selected

    context = {
        'logged_user': logged_user,
        'facilities': facilities,
        'bookings': bookings,
        'restaurant': restaurant,
        'feedbacks': feedbacks,
    }

    return render(request, 'admin_workbench/feedbacks.html', context)

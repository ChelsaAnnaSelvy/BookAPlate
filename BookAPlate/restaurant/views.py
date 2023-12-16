import qrcode
import base64
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from admin_workbench.models import Restaurant, FacilityDetails, BookingDetails, Gallery, Coins,Feedback
from .forms import AboutForm, FacilityDetailsForm, GalleryDetailsForm, EditRestaurantAuthenticationForm, EditRestaurantRegistrationForm,ChangePasswordForm
from django.contrib import messages
from django.contrib.auth import logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required


# Logout view
@login_required
def LogoutView(request):
    """
    Log out the user and redirect to the login page.
    """
    logout(request)
    request.session['logged_out'] = True
    return redirect('login')  

# Home view
@login_required
def HomeView(request):
    """
    Display and update restaurant information for logged-in users.
    """
    logged_user = request.user
    logged_restaurant = Restaurant.objects.filter(user=logged_user).first()
    # Fetch facilities owned by the restaurant
    facilities =FacilityDetails.objects.filter(restaurant=logged_restaurant)

    # Fetch bookings associated with the facilities
    bookings = BookingDetails.objects.filter(facility__in=facilities)

    # Fetch feedbacks associated with the bookings
    feedbacks = Feedback.objects.filter(booking__in=bookings)
    count=feedbacks.count()
    rating= 0
    if count !=0:
        for feedback in feedbacks:
            rating= rating+feedback.rating
        rating=rating/count
    galleries=Gallery.objects.filter(restaurant=logged_restaurant)
    if logged_restaurant:
        if request.method == 'POST':
            form = AboutForm(request.POST, instance=logged_restaurant)
            if form.is_valid():
                form.save()
                return redirect('restaurant_home')
        else:
            form = AboutForm(instance=logged_restaurant)
            context= {
                'form': form, 
                'logged_user': logged_user,
                'restaurant':logged_restaurant,
                'menu_galleries':galleries.filter(category='Menu'),
                'restaurant_galleries':galleries.filter(category='Gallery'),
                'feedbacks':feedbacks,
                'overall_rating':rating,
                'review_count':feedbacks.count(),
                }
            return render(request, 'restaurant/home.html', context)
    else:
        return redirect('login')

# Profile details view
@login_required
def ProfileDetailsView(request):
    """
    Display and update user and restaurant profile details.
    """
    logged_user = request.user
    logged_restaurant = Restaurant.objects.filter(user=logged_user).first()

    if request.method == 'POST':
        userform = EditRestaurantAuthenticationForm(request.POST, instance=logged_user)
        restaurantdetailsform = EditRestaurantRegistrationForm(request.POST, request.FILES, instance=logged_restaurant)

        if userform.is_valid() and restaurantdetailsform.is_valid():
            user = userform.save()
            restaurant = restaurantdetailsform.save(commit=False)
            restaurant.user = user
            restaurant.save()
            messages.success(request, 'You have successfully updated your restaurant details')
            return redirect('restaurant_home')

    else:
        userform = EditRestaurantAuthenticationForm(instance=logged_user)
        restaurantdetailsform = EditRestaurantRegistrationForm(instance=logged_restaurant)
        context = {
            'logged_user': logged_user,
            'restaurant': logged_restaurant,
            'form': userform,
            'form1': restaurantdetailsform,
        }
        return render(request, 'restaurant/update_profile.html', context)

    return redirect('restaurant_home')

# Gallery details view
@login_required
def GalleryDetailsView(request):
    """
    Display and manage restaurant gallery items.
    """
    logged_user = request.user
    logged_restaurant = Restaurant.objects.filter(user=logged_user).first()

    if logged_restaurant:
        if request.method == 'POST':
            form = GalleryDetailsForm(request.POST, request.FILES)
            if form.is_valid():
                gallery = form.save(commit=False)
                gallery.restaurant = logged_restaurant
                gallery.save()
                messages.success(request, 'A new item is successfully added to the gallery.')
                return redirect('gallery_details')
            else:
                form = GalleryDetailsForm()
                return render(request, 'restaurant/gallery.html', {'form': form, 'logged_user': logged_restaurant})
        else:
            form = GalleryDetailsForm()
            galleries = Gallery.objects.filter(restaurant=logged_restaurant)
            menu_galleries = Gallery.objects.filter(restaurant=logged_restaurant, category='Menu')
            photo_galleries = Gallery.objects.filter(restaurant=logged_restaurant, category='Gallery')

            context = {
                'form': form,
                'logged_user': logged_user,
                'menu_galleries': menu_galleries,
                'photo_galleries': photo_galleries,
                'galleries': galleries,
                'count': galleries.count()
            }
            return render(request, 'restaurant/gallery.html', context)
    else:
        return redirect('login')

# Delete gallery item
@login_required
def DeleteGalleryItem(request):
    """
    Delete a gallery item.
    """
    logged_user = request.user
    logged_restaurant = Restaurant.objects.filter(user=logged_user).first()

    if logged_restaurant:
        if request.method == 'POST':
            gallery_id = request.POST.get('gallery_id', 0)
            gallery = get_object_or_404(Gallery, gallery_id=gallery_id)
            gallery.delete()
            messages.success(request, 'An item is successfully deleted from the gallery.')
            return redirect('gallery_details')
    else:
        return redirect('login')

# Edit gallery item
@login_required
def EditGalleryItem(request):
    """
    Edit details of a gallery item.
    """
    logged_user = request.user
    logged_restaurant = Restaurant.objects.filter(user=logged_user).first()

    if logged_restaurant:
        if request.method == 'POST':
            gallery_id = request.POST.get('gallery_id', 0)
            gallery = get_object_or_404(Gallery, gallery_id=gallery_id)
            form = GalleryDetailsForm(request.POST, request.FILES, instance=gallery)

            if form.is_valid():
                form.save()
                messages.success(request, 'The details of a gallery item is successfully updated.')
                return redirect('gallery_details')
            else:
                form = GalleryDetailsForm(instance=gallery)
                context = {
                    'form': form,
                    'logged_user': logged_restaurant,
                    'gallery': gallery
                }
                return render(request, 'restaurant/update_gallery.html', context)
    else:
        return redirect('login')

# Facility details view
@login_required
def FacilityDetailsView(request):
    """
    Display and manage restaurant facility details.
    """
    logged_user = request.user
    logged_restaurant = Restaurant.objects.filter(user=logged_user).first()

    if logged_restaurant:
        if request.method == 'POST':
            form = FacilityDetailsForm(request.POST)
            if form.is_valid():
                facility_number = form.cleaned_data['facility_number']

                if FacilityDetails.objects.filter(restaurant=logged_restaurant, facility_number=facility_number).exists():
                    messages.error(request, 'Facility with the same number already exists.')
                else:
                    facility = form.save(commit=False)
                    facility.restaurant = logged_restaurant
                    facility.save()
                    messages.success(request, 'A new item is successfully added to the facility.')
                return redirect('facility_details')
            else:
                form = FacilityDetailsForm()
                return render(request, 'restaurant/facility.html', {'form': form, 'logged_user': logged_restaurant})
        else:
            form = FacilityDetailsForm()
            facilities = FacilityDetails.objects.filter(restaurant=logged_restaurant)

            context = {
                'form': form,
                'logged_user': logged_user,
                'facilities': facilities,
            }
            return render(request, 'restaurant/facility.html', context)
    else:
        return redirect('login')

# Delete facility item
@login_required
def DeleteFacilityItem(request):
    """
    Delete a facility item.
    """
    logged_user = request.user
    logged_restaurant = Restaurant.objects.filter(user=logged_user).first()

    if logged_restaurant:
        if request.method == 'POST':
            facility_id = request.POST.get('facility_id', 0)
            facility = get_object_or_404(FacilityDetails, facility_id=facility_id)
            facility.delete()
            messages.success(request, 'An item is successfully deleted from the facility.')
            return redirect('facility_details')
    else:
        return redirect('login')

# Edit facility item
@login_required
def EditFacilityItem(request):
    """
    Edit details of a facility item.
    """
    logged_user = request.user
    logged_restaurant = Restaurant.objects.filter(user=logged_user).first()

    if logged_restaurant:
        if request.method == 'POST':
            facility_id = request.POST.get('facility_id', 0)
            facility = get_object_or_404(FacilityDetails, facility_id=facility_id, 
                                         restaurant=logged_restaurant)
            form = FacilityDetailsForm(request.POST, request.FILES, instance=facility)

            if form.is_valid():
                form.save()
                messages.success(request, 'The details of a facility item is successfully updated.')
                return redirect('facility_details')
            else:
                form = FacilityDetailsForm(instance=facility)
                context = {
                    'form': form,
                    'logged_user': logged_restaurant,
                    'facility': facility
                }
                return render(request, 'restaurant/update_facility.html', context)
    else:
        return redirect('login')

@login_required    
def BookingDetailsView(request):
    logged_user = request.user
    logged_restaurant = Restaurant.objects.filter(user=logged_user).first()
    # Get all booking details for the specified restaurant
    bookings = BookingDetails.objects.filter(facility__restaurant=logged_restaurant).order_by('date').distinct()
    context = {
        'bookings':bookings,
        'booked':bookings.filter(status='Booked'),
        'completed':bookings.filter(status='Completed'),
        'cancelled':bookings.filter(status='Cancelled'),
        'attended':bookings.filter(status='Attended'),
        'logged_user': logged_user,
        'restaurant': logged_restaurant,
        
    }  
   
    return render(request, 'restaurant/booking.html', context)


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
    restaurant = Restaurant.objects.filter(user=logged_user).first()
    if request.method== 'POST':
        booking_id = request.POST['booking_id']
        
        if booking_id != 0 :
            booking= get_object_or_404(BookingDetails,booking_id=booking_id)
            customer=booking.customer
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
            Seats reserved: For {int(booking.coins_spend/10)} People
            
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
            context={
            'booking':booking,
            'logged_user': logged_user,
            'customer': customer,
            'facilities':facilities,  
            'head_count':int(booking.coins_spend/10), 
            'restaurant':restaurant,
            'qr_code':qr_code_base64,  
            }
            return render(request,'restaurant/booking_receipt.html',context)
    
    return render(request,'restaurant/booking_receipt.html')

@login_required
def MarkAsAttendedView(request):
    logged_user = request.user
    logged_restaurant = Restaurant.objects.filter(user=logged_user).first()
    if request.method== 'POST':
        booking_id = request.POST['booking_id']
        
        if booking_id != 0 :
            booking= get_object_or_404(BookingDetails,booking_id=booking_id)
            booking.status='Attended'
            booking.save()
            customer=booking.customer
            rewarding_coins=int((booking.coins_spend/30) *20)
            coins=get_object_or_404(Coins,user=customer)
            coins.coin_quantity=int(coins.coin_quantity+rewarding_coins)
            coins.save()
            messages.success(request,'The status is updated.Now wait for their feedback')
    
    return redirect('reservations')

# View for changing password
@login_required
def ChangePasswordView(request):
    logged_user = request.user
    logged_restaurant = Restaurant.objects.filter(user=logged_user).first()
    if request.method == 'POST':
        form = ChangePasswordForm(logged_user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('restaurant_home')
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
        'restaurant': logged_restaurant,
    }

    return render(request, 'restaurant/change_password.html', context)
            
    
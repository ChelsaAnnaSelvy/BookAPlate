import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import LoginForm, UserAuthenticationForm, CustomerRegistrationForm, RestaurantRegistrationForm, RestaurantAuthenticationForm, ForgotPasswordForm
from django.contrib.auth.models import User
from admin_workbench.models import Customer, Restaurant, Coins
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils.crypto import get_random_string

# Create your views here.

# View for the landing page
def HomeView(request):
    return render(request,'user_authentication/home.html')

# View for showing successful login
def ContactView(request):
    return render(request,'user_authentication/contact.html')

# View for Logging in
def LoginView(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_type = request.POST['user_type']

            # Simplify the code by using get() instead of count()
            customer = Customer.objects.filter(user__username=username, status='Active').first()
            restaurant = Restaurant.objects.filter(user__username=username, status='Active').first()

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user_type == 'customer' and customer:
                    return redirect('customer_home')
                elif user_type == 'restaurant' and restaurant:
                    return redirect('restaurant_home')
                elif user.is_superuser:
                    return redirect('admin_home')
                else:
                    user_type_message = 'Customer' if user_type == 'customer' else 'Restaurant'
                    messages.success(request, f"Sorry, the {user_type_message} with the given credentials does not exist. Kindly register as a {user_type_message.lower()}.")
                    return redirect(user_type.lower())

        else:
            form = LoginForm()
            messages.success(request, 'Invalid username or password')
            return render(request, 'user_authentication/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'user_authentication/login.html', {'form': form})

# View for registering Customers
def CustomerRegistrationView(request):
    if request.method == 'POST':
        userform = UserAuthenticationForm(request.POST)
        customerdetailsform = CustomerRegistrationForm(request.POST, request.FILES)

        if userform.is_valid() and customerdetailsform.is_valid():
            user = userform.save()  # Save the user first
            customer = customerdetailsform.save(commit=False)
            customer.user = user  # Link the customer to the user
            customer.save()  # Save the customer details

            # Simplify the coin creation code
            Coins.objects.create(coin_quantity=2000, user=customer)

            messages.success(request, 'You are successfully registered as a customer.')
            return redirect('login')  # Redirect to login page

    else:
        userform = UserAuthenticationForm()
        customerdetailsform = CustomerRegistrationForm()

    return render(request, 'user_authentication/customer_registration.html', {'form': userform, 'form1': customerdetailsform})

# View for registering Restaurants
def RestaurantRegistrationView(request):
    if request.method == 'POST':
        userform = RestaurantAuthenticationForm(request.POST)
        restaurantdetailsform = RestaurantRegistrationForm(request.POST, request.FILES)

        if userform.is_valid() and restaurantdetailsform.is_valid():
            user = userform.save()  # Save the user first
            restaurant = restaurantdetailsform.save(commit=False)
            restaurant.user = user  # Link the restaurant to the user
            restaurant.save()  # Save the restaurant details

            messages.success(request, 'You have successfully registered as a restaurant. Please be patient while we go through your documents. You can log in to the system once we verify your details. Thank you!!')
            return redirect('home')  # Redirect to home page

    else:
        userform = RestaurantAuthenticationForm()
        restaurantdetailsform = RestaurantRegistrationForm()

    return render(request, 'user_authentication/restaurant_registration.html', {'form': userform, 'form1': restaurantdetailsform})

# View for generating and sending an email with a random code
def generate_and_send(request):
    # Generate a random 6-digit code
    code = get_random_string(length=6, allowed_chars='0123456789')

    email = request.session.get('email', '')
    user = User.objects.filter(email=email).first()  # Check if the user exists

    if user:
        # Send the code to the user's email
        user_email = email
        send_mail(
            'Password Reset Code',
            f'Your reset code is: {code}',
            'from@example.com',
            [user_email],
            fail_silently=False,
        )

        # Store the code temporarily in the session
        request.session['reset_code'] = code
        print(code)  # Avoid printing sensitive information in production
        return redirect('verify_otp')
    else:
        messages.error(request, 'This email is not registered with us. Kindly enter a valid email!!!')
        return redirect('forgot_password')

def ForgotPasswordView(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)    
        if form.is_valid():
            email = form.cleaned_data['email']            
            request.session['email'] = email
            return generate_and_send(request)

    else:
        form = ForgotPasswordForm()

    return render(request, 'user_authentication/forgot_password.html', {'form': form}) 

def VerifyOneTimePassword(request):
    if request.method == 'POST':
        r1 = request.POST.get('r1')
        r2 = request.POST.get('r2')
        r3 = request.POST.get('r3')
        r4 = request.POST.get('r4')
        r5 = request.POST.get('r5')
        r6 = request.POST.get('r6')
        entered_code = r1 + r2 + r3 + r4 + r5 + r6
        print(entered_code)  # Avoid printing sensitive information in production
        # Check the entered code against the stored code
        stored_code = request.session.get('reset_code')

        if entered_code == stored_code:
            # Code is valid, allow the user to reset their password
            return render(request, 'user_authentication/reset_password.html')
        else:
            messages.error(request, 'Invalid code. Please try again.')
    
    return render(request, 'user_authentication/otp.html')

# View for resetting the password


def ResetPasswordView(request):
    email = request.session.get('email', '')
    requested_user = User.objects.filter(email=email).first()

    # Check if the user exists
    if not requested_user:
        messages.error(request, 'User not found. Please try again or start the reset password process again.')
        return redirect('forgot_password')  # Redirect to the forgot password page or wherever you want

    if request.method == 'POST':
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if new_password == confirm_password:
            # Use set_password to handle password hashing
            requested_user.set_password(new_password)
            requested_user.save()
            
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')  # Redirect to home or wherever you want
        else:
            messages.error(request, 'Enter the same password in both fields')
            return redirect('reset_password')

    return render(request, 'user_authentication/reset_password.html')

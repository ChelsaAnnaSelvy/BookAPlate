from django.shortcuts import render,redirect
from .forms import LoginForm,UserAuthenticationForm,CustomerRegistrationForm,RestaurantRegistrationForm
from django.contrib.auth.models  import User
from admin_workbench.models import Customer,Restaurant,Coins
from django.contrib.auth import authenticate, login
from django.contrib import messages


# Create your views here.

# View for the landing page
def HomeView(request):
    return render(request,'user_authentication/home.html')

# View for Logging in
def LoginView(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid(): 
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            customer= Customer.objects.filter(user__username=username,status='Active').count()
            restaurant =Restaurant.objects.filter(user__username= username,status='Active').count()
         
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if customer !=0:
                    customer= Customer.objects.filter(user__username=username,status='Active').count()
                    if customer!=0:
                        customer_data= Customer.objects.filter(user__username=username,status='Active')
                        context={
                            'customer': customer_data,
                            'logged_user':request.user,
                        }
                        return render(request, 'customer/home.html')
                    else:
                        msg="Sorry the User doesnot exist. Kindly reach us through complaints@bookaplate.com"
                        return render(request, 'user_authentication/home.html',{'msg': msg})
                elif restaurant !=0:
                    restaurant =Restaurant.objects.filter(user__username= username,status='Active').count()
                    if restaurant!=0:
                        restaurant_data= Restaurant.objects.filter(user__username=username,status='Active')
                        context={
                            'restaurant': restaurant_data,
                            'logged_user':request.user,
                        }
                        return render(request, 'restaurant/home.html',context)
                    else:
                        msg="Sorry the User doesnot exist. Kindly reach us through complaints@bookaplate.com"
                        return render(request, 'user_authentication/home.html',{'msg': msg}) 

        else:
            form = LoginForm()
            error = "Invalid username or password"
            return render(request, 'user_authentication/login.html', {'form': form, 'error': error})
    else:
        form = LoginForm()
    return render(request, 'user_authentication/login.html', {'form': form})

# View for showing successful login
def SuccessView(request):
    return render(request,'user_authentication/success.html')

#View for registering Customers
def CustomerRegistrationView(request):   
    if request.method == 'POST':
        userform = UserAuthenticationForm(request.POST)       
        customerdetailsform = CustomerRegistrationForm(request.POST, request.FILES)
        
        if userform.is_valid() and customerdetailsform.is_valid():
           
            user = userform.save()  # Save the user first
            customer = customerdetailsform.save(commit=False)
            customer.user = user  # Link the customer to the user
            customer.save()  # Save the customer details
            coin=Coins()
            coin.coin_quantity=2000
            coin.user = customer
            coin.save()
            messages.success(request, 'You are successfully registered as a customer.')
            return redirect('login')  # Redirect to login page

    else:
        userform = UserAuthenticationForm()
        customerdetailsform = CustomerRegistrationForm()
    
    return render(request, 'user_authentication/customer_registration.html', {'form': userform, 'form1': customerdetailsform})
   

#View for registering Restaurants
def RestaurantRegistrationView(request):   
    if request.method == 'POST':
        userform = UserAuthenticationForm(request.POST)
        restaurantdetailsform = RestaurantRegistrationForm(request.POST, request.FILES)
        
        if userform.is_valid() and restaurantdetailsform.is_valid():
           
            user = userform.save()  # Save the user first
            restaurant = restaurantdetailsform.save(commit=False)
            restaurant.user = user  # Link the restaurant to the user
            restaurant.save()  # Save the restaurant details
            messages.success(request, 'You have successfully registered as a restaurant. Please be patient while we go through your documents. You can login to the system once  we verify your details. Thank you!!')
            return redirect('login')  # Redirect to login page

    else:
        userform = UserAuthenticationForm()
        restaurantdetailsform = RestaurantRegistrationForm()
    
    return render(request, 'user_authentication/restaurant_registration.html', {'form': userform, 'form1': restaurantdetailsform})
   
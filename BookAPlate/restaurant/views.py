from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from admin_workbench.models import Restaurant,FacilityDetails,BookingDetails,Feedback,Gallery
from .forms import AboutForm,FacilityDetailsForm,GalleryDetailsForm
from django.contrib import messages

# Create your views here.
def HomeView(request):
    logged_user=request.user
    logged_restaurant= Restaurant.objects.filter(user=logged_user).first()
    if logged_restaurant: 
        if request.method == 'POST':           
            
            form = AboutForm(request.POST, instance=logged_restaurant)
            if form.is_valid():
                form.save()
                return redirect('restaurant_home')
            
        else:        
            form = AboutForm(instance=logged_restaurant)
            return render(request, 'restaurant/home.html', {'form': form,'logged_user':logged_user})
    
    else:
        return redirect('login')


def GalleryDetailsView(request):
    logged_user=request.user
    logged_restaurant= Restaurant.objects.filter(user=logged_user).first()
    if logged_restaurant: 
        if request.method == 'POST': 
            form = GalleryDetailsForm(request.POST,request.FILES)
            if form.is_valid():
                gallery = form.save(commit = False)
                gallery.restaurant= logged_restaurant
                gallery.save()
                messages.success(request, 'A new item is successfully added to the gallery.')
                return redirect('gallery_details')
            
            else:        
                form = GalleryDetailsForm()
                return render(request, 'restaurant/gallery.html', {'form': form,'logged_user':logged_restaurant})
            
        else:        
            form =GalleryDetailsForm()
            galleries=Gallery.objects.filter(restaurant= logged_restaurant)
            menu_galleries=Gallery.objects.filter(restaurant= logged_restaurant,category= 'Menu')
            photo_galleries=Gallery.objects.filter(restaurant= logged_restaurant,category='Gallery')
           
            context={
                'form': form,
                'logged_user':logged_user,
                'menu_galleries': menu_galleries,
                'photo_galleries':photo_galleries,
                'galleries':galleries,
                'count': galleries.count()
                }
            return render(request, 'restaurant/gallery.html', context)
    
    else:
        return redirect('login')

def DeleteGalleryItem(request):
    logged_user=request.user
    logged_restaurant= Restaurant.objects.filter(user=logged_user).first()
    if logged_restaurant: 
        if request.method == 'POST':           
            gallery_id= request.POST.get('gallery_id',0)
            gallery = get_object_or_404(Gallery,gallery_id=gallery_id)
            gallery.delete()
            messages.success(request, 'An item is successfully deleted from the gallery.')
            return redirect('gallery_details')  
    else:
        return redirect('login')

def EditGalleryItem(request):
    logged_user=request.user
    logged_restaurant= Restaurant.objects.filter(user=logged_user).first()
    if logged_restaurant: 
        if request.method == 'POST':           
            gallery_id= request.POST.get('gallery_id',0)
            gallery = get_object_or_404(Gallery,gallery_id=gallery_id)
            form = GalleryDetailsForm(request.POST,request.FILES,instance=gallery)
            if form.is_valid():
                form.save()
                messages.success(request, 'The details of a gallery item is successfully updated.')
                return redirect('gallery_details')
            
            else:        
                form = GalleryDetailsForm(instance=gallery)
                context={
                    'form': form,
                    'logged_user':logged_restaurant,
                    'gallery':gallery
                    }
                return render(request, 'restaurant/update_gallery.html', context)
            
           
    else:
        return redirect('login')

def FacilityDetailsView(request):
    logged_user=request.user
    logged_restaurant= Restaurant.objects.filter(user=logged_user).first()
    if logged_restaurant: 
        if request.method == 'POST':         
            form = FacilityDetailsForm(request.POST)
            if form.is_valid():
                facility = form.save(commit = False)
                facility.restaurant= logged_restaurant
                facility.save()
                messages.success(request, 'A new item is successfully added to the facility.')
                return redirect('facility_details')
            
            else:        
                form = FacilityDetailsForm()
                return render(request, 'restaurant/facility.html', {'form': form,'logged_user':logged_restaurant})
            
        else:        
            form = FacilityDetailsForm()
            facilities=FacilityDetails.objects.filter(restaurant= logged_restaurant)
           
            context={
                'form': form,
                'logged_user':logged_user,
                'facilities': facilities,
                }
            return render(request, 'restaurant/facility.html', context)
    
    else:
        return redirect('login')

def DeleteFacilityItem(request):
    logged_user=request.user
    logged_restaurant= Restaurant.objects.filter(user=logged_user).first()
    if logged_restaurant: 
        if request.method == 'POST':           
            facility_id= request.POST.get('facility_id',0)
            facility = get_object_or_404(FacilityDetails, facility_id =  facility_id)
            facility.delete()
            messages.success(request, 'An item is successfully deleted from the facility.')
            return redirect('facility_details')  
    else:
        return redirect('login')

def EditFacilityItem(request):
    logged_user=request.user
    logged_restaurant= Restaurant.objects.filter(user=logged_user).first()
    if logged_restaurant: 
        if request.method == 'POST':           
            facility_id= request.POST.get('facility_id',0)
            print(facility_id)
            facility = get_object_or_404(FacilityDetails,facility_id=facility_id)
            form = FacilityDetailsForm(request.POST,request.FILES,instance=facility)
            if form.is_valid():
                form.save()
                messages.success(request, 'The details of a facility item is successfully updated.')
                return redirect('facility_details')
            
            else:        
                form = FacilityDetailsForm(instance=facility)
                context={
                    'form': form,
                    'logged_user':logged_restaurant,
                    'facility':facility
                    }
                return render(request, 'restaurant/update_facility.html', context)
            
           
    else:
        return redirect('login')
 
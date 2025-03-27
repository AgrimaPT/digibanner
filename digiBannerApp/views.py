# from django.db.models import Q
# from django.utils import timezone
from django.shortcuts import render,redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Banner
from django.db import models
from django.db.models import Q  # Add this import

import json
from django.http import JsonResponse
from django.utils import timezone
from .models import Banner,BannerMedia
from django.contrib.admin.views.decorators import staff_member_required
from .forms import BannerForm
from django.contrib.auth.decorators import login_required


# @login_required
# def banner_slider(request):
#     now = timezone.now()
    
#     # Query for active banners that are either:
#     # 1. Default banners (no start_time or end_time), or
#     # 2. Scheduled banners that are currently active (start_time <= now <= end_time)
#     banners = Banner.objects.filter(
        
#         active=True
#     ).filter(
#         Q(is_scheduled=False) |  
#         Q(is_scheduled=True, start_time__lte=now, end_time__gte=now)  
#     ).distinct()  
    

#     print("Banners Retrieved:", banners.count())
#     for banner in banners:
#         print(f"ID: {banner.id}, Title: {banner.title}, Start: {banner.start_time}, End: {banner.end_time}, Active: {banner.active}")

#     return render(request, 'banner.html', {'banners': banners})

# def banner_data(request):
#     now = timezone.now()
    
#     banners = Banner.objects.filter(
        
#         active=True
#     ).filter(
#         Q(is_scheduled=False) |  # Default banners
#         Q(is_scheduled=True, start_time__lte=now, end_time__gte=now)  # Scheduled banners within their time range
#     ).order_by('-id')

#     # # Print banner details for debugging
#     # for banner in banners:
#     #     print(f"Banner: {banner.title}, Scheduled: {banner.is_scheduled}, Start: {banner.start_time}, End: {banner.end_time}")
    
#     data = {
#         "banners": [
#             {
#                 "id": banner.id,
#                 "title": banner.title,
#                 "media_urls": [media.media.url for media in banner.media_files.all()],
#             }
#             for banner in banners
#         ]
#     }
    
#     return JsonResponse(data)

# @staff_member_required

# @login_required
# @login_required(login_url='login')
# def custom_banner_admin(request):
#     user = request.user  # Get the logged-in user

#     if request.method == 'POST':
#         form = BannerForm(request.POST)
#         files = request.FILES.getlist('media_files')

#         if form.is_valid():
#             banner = form.save(commit=False)
#             banner.user = request.user  # Assign the banner to the logged-in user
#             banner.save()

#             for file in files:
#                 BannerMedia.objects.create(banner=banner, media=file)

#             messages.success(request, "Banner added successfully with multiple media files!")
#             return redirect('custom_banner_admin')
#         else:
#             messages.error(request, "Error adding banner. Please check the details below.")
#     else:
#         form = BannerForm()

#     # **Filter banners only for the logged-in user**
#     banners = Banner.objects.filter(user=user).prefetch_related('media_files')

#     print(f"User: {user.username}, Banners Count: {banners.count()}")  # Debugging

#     return render(request, 'custom_banner_admin.html', {'form': form, 'banners': banners,'user':user})



def banner_slider(request, username=None):
    now = timezone.now()

    # Get the user (either from request or username in URL)
    user = get_object_or_404(User, username=username)
    # if username:
    #     user = get_object_or_404(User, username=username)
    # else:
    #     user = request.user

    # Query banners only for this user
    banners = Banner.objects.filter(
        user=user,  # Ensure only banners for this user are retrieved
        active=True
    ).filter(
        Q(is_scheduled=False) |  # Default banners
        Q(is_scheduled=True, start_time__lte=now, end_time__gte=now)  # Scheduled banners
    ).distinct()

    return render(request, 'banner.html', {'banners': banners, 'user': user})


def banner_data(request, username=None):
    now = timezone.now()


    user = get_object_or_404(User, username=username)
    # if username:
    #     user = get_object_or_404(User, username=username)
    # else:
    #     if not request.user.is_authenticated:
    #         return JsonResponse({"error": "User not authenticated"}, status=403)
    #     user = request.user  # Use logged-in user


    # Filter banners for the specific user
    banners = Banner.objects.filter(
        user=user,
        active=True
    ).filter(
        Q(is_scheduled=False) |  
        Q(is_scheduled=True, start_time__lte=now, end_time__gte=now)
    ).order_by('-id')

    data = {
        "banners": [
            {
                "id": banner.id,
                "title": banner.title,
                "media_urls": [media.media.url for media in banner.media_files.all()],
            }
            for banner in banners
        ]
    }
    return JsonResponse(data)


@login_required(login_url='login')
def custom_banner_admin(request, username):
    # Get the user object based on the username in the URL
    user = get_object_or_404(User, username=username)

    # Check if the logged-in user is trying to access their own dashboard
    # if request.user != user:
    #     messages.error(request, "❌ You do not have permission to access this page.")
    #     return redirect('custom_banner_admin', username=request.user.username)

    if request.method == 'POST':
        form = BannerForm(request.POST)
        files = request.FILES.getlist('media_files')

        if form.is_valid():
            banner = form.save(commit=False)
            banner.user = user  # Assign banner to the correct user
            banner.save()

            # ✅ Handling multiple file uploads
            for file in files:
                BannerMedia.objects.create(banner=banner, media=file)

            messages.success(request, "✅ Banner added successfully !")
            return redirect('custom_banner_admin', username=user.username)  # Redirect to the correct user’s dashboard
        else:
            messages.error(request, "❌ Error adding banner. Please check your input.")

    else:
        form = BannerForm()

    # ✅ **Filter banners only for the correct user**
    banners = Banner.objects.filter(user=user).prefetch_related('media_files')

    return render(request, 'custom_banner_admin.html', {
        'form': form,
        'banners': banners,
        'user': user
    })


@require_POST
def update_banner_active(request, banner_id,username):
    banner = get_object_or_404(Banner, pk=banner_id)
    user = get_object_or_404(User, username=username)

    # Check the POST data to see if the checkbox was checked.
    # A checked checkbox sends "on", otherwise it won't be in POST.
    banner.active = 'active' in request.POST or request.POST.get('active') == 'on'
    banner.save()

    
    return redirect(reverse('custom_banner_admin', kwargs={'username': user.username}))
       
    # return redirect('custom_banner_admin')
    

@require_POST
def delete_banner(request, banner_id,username):
    user = get_object_or_404(User, username=username)

    banner = get_object_or_404(Banner, pk=banner_id)
    banner.delete()
    # return redirect('custom_banner_admin')
    return redirect(reverse('custom_banner_admin', kwargs={'username': user.username}))
       


from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from .models import Banner
from .forms import BannerForm

def edit_banner(request, banner_id):
    banner = get_object_or_404(Banner, id=banner_id)
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            banner = form.save(commit=False)
            
            # If start_time or end_time is missing, set is_scheduled to False
            if not banner.start_time or not banner.end_time:
                banner.is_scheduled = False
            else:
                banner.is_scheduled = True
            banner.active = request.POST.get('active') == 'true'
            banner.save()
            # form.save()  # Updates the model.
            data = {
                'banner_id': banner.id,
                'title': banner.title,
                'is_scheduled':banner.is_scheduled,
                'active':banner.active,
                'start_date': banner.start_time.strftime('%Y-%m-%d') if banner.start_time else '',
                'start_time_input': banner.start_time.strftime('%I:%M %p') if banner.start_time else '',
                'end_date': banner.end_time.strftime('%Y-%m-%d') if banner.end_time else '',
                'end_time_input': banner.end_time.strftime('%I:%M %p') if banner.end_time else '',
            }
           
            return JsonResponse(data)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    
    else:
        # Since editing is done via AJAX in the modal, no separate GET template is needed.
        return HttpResponse(status=405)
    
    
from django.views.decorators.http import require_http_methods
@require_http_methods(["DELETE"])
def delete_media(request, media_id):
    try:
        media = BannerMedia.objects.get(id=media_id)  # Use the `id` field
        media.delete()  # Delete the media file
        return JsonResponse({'status': 'success', 'message': 'Media deleted successfully.'})
    except BannerMedia.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Media not found.'}, status=404)
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def delete_selected_media(request):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            media_ids = data.get('media_ids', [])

            if not media_ids:
                return JsonResponse({'error': 'No media IDs provided'}, status=400)
            
            BannerMedia.objects.filter(id__in=media_ids).delete()

            return JsonResponse({'message': 'Media files deleted successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def add_media(request, banner_id):
    if request.method == 'POST':
        banner = Banner.objects.get(id=banner_id)
        for file in request.FILES.getlist('media_files'):
            BannerMedia.objects.create(banner=banner, media=file)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def get_media_files(request, banner_id):
    # Fetch the banner object
    banner = get_object_or_404(Banner, id=banner_id)
    
    # Fetch all media files associated with the banner
    media_files = banner.media_files.all()  # Adjust based on your model relationship
    
    # Prepare the response data
    media_data = [
        {
            'id': media.id,
            'url': media.media.url,  # Assuming `media` is a FileField or ImageField
            'type': 'video' if media.media.url.lower().endswith('.mp4') else 'image'
        }
        for media in media_files
    ]
    
    return JsonResponse({'media_files': media_data})


from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            messages.error(request, "Your password and confirm password do not match!")
            return redirect('signup')

        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username is already taken. Please choose another.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered. Try logging in instead.")
            return redirect('signup')

        try:
            my_user = User.objects.create_user(username=uname, email=email, password=pass1)
            my_user.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('signup')

    return render(request, 'users/signup.html')
from django.urls import reverse

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        
        # Basic validation
        if not username or not pass1:
            messages.error(request, "Both username and password are required!")
        else:
            user = authenticate(request, username=username, password=pass1)
            if user is not None:
                login(request, user)
                return redirect(reverse('custom_banner_admin', kwargs={'username': user.username}))
            else:
                messages.error(request, "Invalid username or password!")
        
        # Return to login page with messages
        return redirect('login')  # Assuming 'login' is your URL name

    return render(request, 'users/login.html')


def LogoutPage(request):
    logout(request)
    return redirect('login')
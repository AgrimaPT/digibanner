# from django.db.models import Q
# from django.utils import timezone
from django.shortcuts import render,redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
# from .models import Banner

# def banner_slider(request):
#     now = timezone.now()
#     # Query for banners with a time range that are currently active.
#     timed_banners = Banner.objects.filter(
#         active=True,
#         start_time__lte=now,
#         end_time__gte=now
#     )
#     if timed_banners.exists():
#         # If any scheduled banners are active, display them.
#         banners = timed_banners
#     else:
#         # Otherwise, display the always-on banners.
#         banners = Banner.objects.filter(active=True, start_time__isnull=True, end_time__isnull=True)
#     return render(request, 'banner.html', {'banners': banners})

# views.py
import json
from django.http import JsonResponse
from django.utils import timezone
from .models import Banner
from django.contrib.admin.views.decorators import staff_member_required
from .forms import BannerForm

def banner_slider(request):
    now = timezone.now()
    # Query for banners with a time range that are currently active.
    timed_banners = Banner.objects.filter(
        active=True,
        start_time__lte=now,
        end_time__gte=now
    )
    if timed_banners.exists():
        # If any scheduled banners are active, display them.
        banners = timed_banners
    else:
        # Otherwise, display the always-on banners.
        banners = Banner.objects.filter(active=True, start_time__isnull=True, end_time__isnull=True)
    return render(request, 'banner.html', {'banners': banners})

def banner_data(request):
    now = timezone.now()
    # Priority: scheduled banners if any are active, otherwise default banners.
    timed_banners = Banner.objects.filter(active=True, start_time__lte=now, end_time__gte=now)
    if timed_banners.exists():
        banners = timed_banners
    else:
        banners = Banner.objects.filter(active=True, start_time__isnull=True, end_time__isnull=True)

    # Serialize banner data.
    banner_list = []
    for banner in banners:
        banner_list.append({
            'id': banner.id,
            'title': banner.title,
            'media_url': banner.media.url if banner.media else '',
            # 'url': banner.url,
        })
    return JsonResponse({'banners': banner_list})

@staff_member_required
def custom_banner_admin(request):
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Banner added successfully!")
            return redirect('custom_banner_admin')
        else:
            messages.error(request, "There was an error adding the banner. Please check the details below.")
    else:
        form = BannerForm()
    # Retrieve all banners (you could also paginate or filter as needed)
    banners = Banner.objects.all()
    return render(request, 'custom_banner_admin.html', {'form': form, 'banners': banners})


@require_POST
def update_banner_active(request, banner_id):
    banner = get_object_or_404(Banner, pk=banner_id)
    # Check the POST data to see if the checkbox was checked.
    # A checked checkbox sends "on", otherwise it won't be in POST.
    banner.active = 'active' in request.POST or request.POST.get('active') == 'on'
    banner.save()
    return redirect('custom_banner_admin')

@require_POST
def delete_banner(request, banner_id):
    banner = get_object_or_404(Banner, pk=banner_id)
    banner.delete()
    return redirect('custom_banner_admin')

# def edit_banner(request, banner_id):
#     banner = get_object_or_404(Banner, id=banner_id)
#     if request.method == 'POST':
#         form = BannerForm(request.POST, request.FILES, instance=banner)
#         if form.is_valid():
#             form.save()
#             return redirect('custom_banner_admin')
#     else:
#         form = BannerForm(instance=banner)
#     return render(request, 'edit_banner.html', {'form': form, 'banner': banner})

from django.http import JsonResponse

# def edit_banner(request, banner_id):
#     banner = get_object_or_404(Banner, id=banner_id)
#     if request.method == 'POST':
#         form = BannerForm(request.POST, request.FILES, instance=banner)
#         if form.is_valid():
#             form.save()  # This updates the model.
#             # Check if the request is AJAX:
#             if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#                 data = {
#                     'banner_id': banner.id,
#                     'title': banner.title,
#                     'start_time': banner.start_time.strftime('%Y-%m-%dT%H:%M') if banner.start_time else '',
#                     'end_time': banner.end_time.strftime('%Y-%m-%dT%H:%M') if banner.end_time else ''
#                 }
#                 return JsonResponse(data)
#             else:
#                 return redirect('custom_banner_admin')
#     else:
#         form = BannerForm(instance=banner)
#     return render(request, 'edit_banner.html', {'form': form, 'banner': banner})

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from .models import Banner
from .forms import BannerForm

def edit_banner(request, banner_id):
    banner = get_object_or_404(Banner, id=banner_id)
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            form.save()  # Updates the model.
            data = {
                'banner_id': banner.id,
                'title': banner.title,
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


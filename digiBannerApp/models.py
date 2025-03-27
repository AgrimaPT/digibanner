from django.contrib.auth.models import User
from django.db import models

class Banner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    title = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    is_scheduled = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

class BannerMedia(models.Model):
    banner = models.ForeignKey(Banner, related_name='media_files', on_delete=models.CASCADE)
    media = models.FileField(upload_to='banners/')

    def __str__(self):
        return f"Media for {self.banner.title}"
    


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     organization_name = models.CharField(max_length=255)  # Add restaurant name
#     logo = models.ImageField(upload_to='media/restaurant_logos/', null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.organization_name


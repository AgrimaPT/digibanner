from django.db import models
from django.utils import timezone

class BannerGroup(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)  # Represents group-level active status

    def __str__(self):
        return self.name

class Banner(models.Model):
    title = models.CharField(max_length=200, blank=True)
    # image = models.ImageField(upload_to='banners/')
    media = models.FileField(upload_to='banners/', blank=True, null=True)
    group = models.ForeignKey(BannerGroup, on_delete=models.SET_NULL, null=True, blank=True)
    # Optional time fields: if left empty, the banner is always shown.
    start_time = models.DateTimeField(
        null=True, blank=True, 
        help_text="Optional: start time for scheduled banner display"
    )
    end_time = models.DateTimeField(
        null=True, blank=True, 
        help_text="Optional: end time for scheduled banner display"
    )
    active = models.BooleanField(default=True, help_text="Enable/disable banner")

    def is_timed(self):
        return self.start_time is not None and self.end_time is not None

    def is_active(self):
        now = timezone.now()
        if self.is_timed():
            return self.active and self.start_time <= now <= self.end_time
        return self.active  # Always active if no time limits are provided

    def __str__(self):
        return self.title or "Banner #{}".format(self.id)

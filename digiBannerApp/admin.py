from django.contrib import admin
from .models import Banner
# Register your models here.
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'start_time', 'end_time')
    list_filter = ('active',)
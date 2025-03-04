# from django.urls import path
# from . import views

# urlpatterns = [
#     path('banner_view/', views.banner_slider, name='banner_view'),
# ]

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('banner_view/', views.banner_slider, name='banner_slider'),
    path('banner_data/', views.banner_data, name='banner_data'),
    path('custom-admin/', views.custom_banner_admin, name='custom_banner_admin'),
    path('banner/update/<int:banner_id>/', views.update_banner_active, name='update_banner_active'),
    path('banner/delete/<int:banner_id>/', views.delete_banner, name='delete_banner'),
    path('banner/edit/<int:banner_id>/', views.edit_banner, name='edit_banner'),
    

]

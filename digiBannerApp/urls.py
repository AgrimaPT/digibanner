# from django.urls import path
# from . import views

# urlpatterns = [
#     path('banner_view/', views.banner_slider, name='banner_view'),
# ]

# urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('logout/',views.LogoutPage,name='logout'),

    path('custom-admin/<str:username>/', views.custom_banner_admin, name='custom_banner_admin'),
    path('banner_view/<str:username>/', views.banner_slider, name='banner_slider'),
    path('banner_data/<str:username>/', views.banner_data, name='banner_data'),

    # path('banner_view/', views.banner_slider, name='banner_slider'),
    # path('banner_data/', views.banner_data, name='banner_data'),
    # path('custom-admin/', views.custom_banner_admin, name='custom_banner_admin'),
    path('banner/update/<int:banner_id>/<str:username>/', views.update_banner_active, name='update_banner_active'),
    path('banner/delete/<int:banner_id>/<str:username>/', views.delete_banner, name='delete_banner'),
    path('banner/edit/<int:banner_id>/', views.edit_banner, name='edit_banner'),
    
    path('delete-media/<int:media_id>/', views.delete_media, name='delete_media'),

    path('delete_selected_media/', views.delete_selected_media, name='delete_media'),
    path('get-media-files/<int:banner_id>/', views.get_media_files, name='get_media_files'),
    path('add-media/<int:banner_id>/', views.add_media, name='add_media'),   
]

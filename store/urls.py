
from django.urls import path, include
from . import views

urlpatterns = [
    path('categories/<str:category>/', views.get_main_page),
    path('items/<int:id>', views.get_item_page),
    path('accounts/profile/', views.get_user_page),
    path('user/update/', views.update_user),
    path('user/signup/', views.get_signup_page),
    path('user/new_user/', views.create_user),
    path('items/addToCart/', views.add_to_cart),
    path('updatecart/<int:id>', views.update_cart),
    path('', include("django.contrib.auth.urls")),
    path('', views.get_home_page),
]
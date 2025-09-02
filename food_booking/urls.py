from django.urls import path
from . import views, owner_views

app_name = 'food_booking'

urlpatterns = [
    path('', views.menu_view, name='menu'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('order/', views.order_form, name='order_form'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('api/add-to-cart/', views.api_add_to_cart, name='api_add_to_cart'),
    
    # Owner/Admin URLs
    path('owner/', owner_views.owner_dashboard, name='owner_dashboard'),
    path('owner/orders/', owner_views.owner_orders, name='owner_orders'),
    path('owner/orders/<int:order_id>/', owner_views.owner_order_detail, name='owner_order_detail'),
    path('owner/food-items/', owner_views.owner_food_items, name='owner_food_items'),
    path('owner/food-items/add/', owner_views.owner_add_food_item, name='owner_add_food_item'),
    path('owner/food-items/<int:item_id>/edit/', owner_views.owner_edit_food_item, name='owner_edit_food_item'),
    path('owner/analytics/', owner_views.owner_analytics, name='owner_analytics'),
    path('owner/settings/', owner_views.owner_settings, name='owner_settings'),
]

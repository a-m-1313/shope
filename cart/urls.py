from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail_view, name='cart_detail_view'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart_view'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_cart'),
    path('update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('clear', views.clear_cart, name='clear_cart'),
]

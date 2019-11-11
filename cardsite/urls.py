
from django.urls import path, include
from .views import (
    ItemDetailView, 
    CheckoutView, HomeView, 
    add_to_cart, 
    remove_from_cart,
    remove_single_item_from_cart,
    PaymentView,
    order_summary_view,
    ApplyCoupon
    )

app_name = 'cardsite'

urlpatterns = [
    path('', HomeView.as_view(), name='item-list'),
    path('product/<slug>/', ItemDetailView.as_view() , name='product'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('apply-coupon', ApplyCoupon.as_view(), name='apply-coupon'),
    
    path('order-summary', order_summary_view.as_view(), name='order-summary'),
    path('remove-single-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment')
]
from django.contrib import admin

# Register your models here.

from .models import Item, OrderItem, Order, BillingAddress,Payment, Coupon, Card

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'ordered']


class CardAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'code', 'active']


class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', '__str__', 'getAvail']

admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(BillingAddress)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Card, CardAdmin)
from django.contrib import admin

# Register your models here.

from .models import Item, OrderItem, Order, BillingAddress,Payment, Coupon

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'ordered']

admin.site.register(Item)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(BillingAddress)
admin.site.register(Payment)
admin.site.register(Coupon)
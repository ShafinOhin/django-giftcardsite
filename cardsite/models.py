from django.db import models
from django.conf import settings
from django.shortcuts import reverse


class Card(models.Model):
    active = models.BooleanField(default=True)
    code = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class UsedCard(models.Model):
    active = models.BooleanField(default=False)
    code = models.CharField(max_length=30)
    description = models.TextField()
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title


CATAGORY_CHOICES = (
    ('GP', 'Google Play'),
    ('AM', 'AMAZON'),
    ('NF', 'NETFLIX'),
    ('IT', 'ITUNES'),
    ('ST', 'STEAM')
)



class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    catagory = models.CharField(choices=CATAGORY_CHOICES, max_length=2)
    iscode = models.BooleanField(default=True)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to='pics')
    gift_cards = models.ManyToManyField(Card, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cardsite:product', kwargs={
            'slug': self.slug
        })
    def get_add_to_cart_url(self):
        return reverse('cardsite:add-to-cart', kwargs={
            'slug': self.slug
        })
    def get_remove_from_cart_url(self):
        return reverse('cardsite:remove-from-cart', kwargs={
            'slug': self.slug
        })


    def getAvail(self):
        return self.gift_cards.all().count()


    def isAvail(self):
        if self.gift_cards.all():
            return True
        else:
            return False


    def get_label_text(self):
        if self.isAvail():
            return 'In stock'
        else:
            return 'Sold out'
    

    def get_label_color(self):
        if self.isAvail():
            return 'primary'
        else:
            return 'danger'

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"


    def get_total_item_price(self):
        return self.item.price * self.quantity

    def get_total_discount_item_price(self):
        return self.item.discount_price * self.quantity

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        else:
            return self.get_total_item_price()



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add = True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    final_cards = models.ManyToManyField(UsedCard, blank=True)

    def __str__(self):
        return self.user.username


    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total = total + order_item.get_final_price()
        if self.coupon:
            if self.coupon.lessen == 0:
                total -= ((self.coupon.percent * total)/100)
            else:
                total -= self.coupon.lessen
        return float(int(total))
    

    def get_discount(self):
        total = 0
        ret = 0
        for order_item in self.items.all():
            total = total + order_item.get_final_price()
        if self.coupon:
            if self.coupon.lessen == 0:
                ret = ((self.coupon.percent * total)/100)
            else:
                ret = self.coupon.lessen

        return ret
    

    def get_order_no(self):
        return str(self.id)[::-1] + self.user.username[::-1].upper()


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=11, default=None)


    def __str__(self):
        return self.user.username



class Payment(models.Model):
    phone = models.CharField(max_length=11)
    trxid = models.CharField(max_length=20)
    amount = models.IntegerField(default=0)





class Coupon(models.Model):
    code = models.CharField(max_length=15)
    percent = models.IntegerField()
    lessen = models.IntegerField()
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    used_by = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    oneuse = models.BooleanField(default=True)

    def __str__(self):
        return self.code




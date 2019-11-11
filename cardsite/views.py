from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order
from django.utils import timezone
from .forms import CheckoutForm, PaymentForm, CouponForm
from .models import BillingAddress, Payment, Coupon
# Create your views here.


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = 'home.html'

class ItemDetailView(DetailView):
    model = Item
    template_name = 'product.html'


class order_summary_view(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
        except ObjectDoesNotExist:
            messages.warning(self.request, "You don't have an active order")
            return redirect("/")
        return render(self.request, 'order-summary.html', context)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            order_items = order.items.all()
            context = {
                'form' : form,
                'order_items' : order_items,
                'order' : order,
                'couponForm' : CouponForm(),
                'showCoupon' : True
            }
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You don't have an active order")
            return redirect("cardsite:order-summary")
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)


        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                phone = form.cleaned_data.get('phone')
                # TODO add functionalities for these fields
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user = self.request.user,
                    email = email,
                    phone = phone
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                if payment_option == 'B':
                    return redirect('cardsite:payment', payment_option='bkash')
                elif payment_option == 'R':
                    return redirect('cardsite:payment', payment_option='rocket')
                else:
                    messages.warning(self.request, "Invalid payment option selected")
                    return redirect('cardsite:checkout')
            else:
                messages.warning(self.request, 'Please fill the form correctly!')
                return redirect('cardsite:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You don't have an active order")
            return redirect("cardsite:order-summary")


class PaymentView(View):
    def get(self, *args, **kwargs):
        form = PaymentForm()
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            order_items = order.items.all()
            context = {
                'form' : form,
                'order_items' : order_items,
                'order' : order,
                'showCoupon' : False
            }
            return render(self.request, 'payment.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, 'Do not do that!')
            return redirect('cardsite:order-summary')
    def post(self, *args, **kwargs):
        form = PaymentForm(self.request.POST or None)
        if form.is_valid() == False:
            messages.warning(self.request, 'Input not valid!')
            # TODO correct payment_option, can be also rocket.
            return redirect('cardsite:payment', payment_option = 'bkash')
        if form.cleaned_data.get('trxid') == 'iamsopoor':
            try:
                order = Order.objects.get(user=self.request.user, ordered=False)
                if form.is_valid():
                    phone = form.cleaned_data.get('phone')
                    trxid = form.cleaned_data.get('trxid')
                    payment = Payment(
                        phone = phone,
                        trxid = trxid,
                        amount = order.get_total()
                    )
                    payment.save()
                    order.payment = payment
                    order.ordered = True
                    order_items = order.items.all()
                    order_items.update(ordered=True)
                    for item in order_items:
                        item.save()
                    order.save()
                    messages.success(self.request, 'Payment successfull, Order placed')
                    print("Order placed")
                    return redirect('cardsite:item-list')
                
            except ObjectDoesNotExist:
                messages.warning(self.request, "You don't have an active order")
                return redirect("cardsite:order-summary")
        else:
            messages.warning(self.request, 'Transaction ID not valid!')
            return redirect('cardsite:payment', payment_option='bkash')



@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(user=request.user, item=item, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated")
            return redirect('cardsite:order-summary')
        else:
            messages.info(request, "This item was added to your cart")
            order.items.add(order_item)
            return redirect('cardsite:order-summary')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
        return redirect('cardsite:order-summary')


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(user=request.user, item=item, ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request, "item removed from your cart")
            return redirect('cardsite:order-summary')
        else:
            messages.info(request, "Your cart doesn't contain this item")
            return redirect('cardsite:order-summary')
            
    else:
        messages.info(request, "You don't have an existing order")
        return redirect('cardsite:order-summary')


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(user=request.user, item=item, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            return redirect('cardsite:order-summary')
        else:
            messages.info(request, "Your cart doesn't contain this item")
            return redirect('cardsite:order-summary', slug=slug)
            
    else:
        messages.info(request, "You don't have an existing order")
        return redirect('cardsite:product', slug=slug)



def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "Invalid coupon")
        return redirect('cardsite:checkout')


class ApplyCoupon(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(user=self.request.user, ordered=False)
                coupon = get_coupon(self.request, code)
                now = timezone.now()
                if coupon.oneuse:
                    if coupon.date_from<=now and coupon.date_to>=now:
                        if coupon.is_active:
                            if coupon.used_by.all().filter(username=self.request.user.username):
                                messages.warning(self.request, "You have already used this coupon")
                                return redirect('cardsite:checkout')
                            else:
                                order.coupon = coupon
                                order.save()
                                messages.success(self.request, "Coupon applied succesfully")
                                return redirect('cardsite:checkout')
                        else:
                            messages.warning(self.request, "Coupon code is not active now")
                            return redirect('cardsite:checkout')
                    else:
                        messages.warning(self.request, "Coupon Code expired")
                        return redirect('cardsite:checkout')
                    
                else:
                    if coupon.date_from<=now and coupon.date_to>=now:
                        if coupon.is_active:
                            order.coupon = coupon
                            order.save()
                            messages.success(self.request, "Coupon applied succesfully")
                            return redirect('cardsite:checkout')
                        else:
                            messages.warning(self.request, "Coupon code not active now")
                            return redirect('cardsite:checkout')
                    else:
                        messages.warning(self.request, "Coupon Code expired")
                        return redirect('cardsite:checkout')


            except ObjectDoesNotExist:
                messages.info(self.request, "You don't have an existing order")
                return redirect('cardsite:checkout')
        else:
            messages.warning(self.request, 'Some error occured')
            return redirect('cardsite:checkout')

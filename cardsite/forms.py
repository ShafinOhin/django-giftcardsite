from django import forms
from django_countries.fields import CountryField
from django.contrib import auth
from django.core.validators import RegexValidator


PAYMENT_CHOICES = (
    ('B', 'Bkash'),
    ('R', 'Rocket')
)

class CheckoutForm(forms.Form):
    #streetAddress = forms.CharField()
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder' : ''
    }))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': '01XXXXXXXXXXX',
        
    }))
    #apartmentAddress = forms.CharField(required=False)
    #country = CountryField(blank_label='(select country)')
    #zip = forms.CharField()
    #same_billing_address = forms.BooleanField(widget=forms.CheckboxInput())
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)



class PaymentForm(forms.Form):
    phone = forms.CharField(validators=[RegexValidator("^(01){1}[0-9]{9}$")], widget=forms.TextInput(attrs={
        'placeholder': '01XXXXXXXXX'
    }))
    trxid = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'placeholder': ' '
    }))


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Promo code',
        'area-label' : "Recipient's username",
        'aria-describedby' : 'basic-addon2'
    }))

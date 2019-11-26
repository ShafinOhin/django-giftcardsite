from django.shortcuts import render


def encoder(request):
    return render(request, 'encoder/encoder.html')
from django.shortcuts import render

def main(request):
    return render(request, 'index.html')

def products(request):
    return render(request, 'products.html')

def contact(request):
    return render(request, 'contact.html')
# Create your views here.

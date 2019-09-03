from django.shortcuts import render
import datetime
from .models import ProductCategory, Product


def main(request):
    title = 'Main'

    products = Product.objects.all()

    content = {'title': title, 'products': products}
    return render(request, 'index.html', content)


def products(request, pk=None):
    title = 'Products'

    products = Product.objects.all()
    products_category = ProductCategory.objects.all()

    content = {'title': title, 'products_category': products_category,
               'products': products}
    return render(request, 'products.html', content)


def contact(request):
    title = 'Contact'

    visit_date = datetime.datetime.now()
    locations = [
        {
            'city': 'Москва',
            'phone': '+7-888-888-8888',
            'email': 'info@interiorshop.ru',
            'address': 'В пределах МКАД',
        },
        {
            'city': 'Екатеринбург',
            'phone': '+7-777-777-7777',
            'email': 'info_yekaterinburg@interiorshop.ru',
            'address': 'Близко к центру',
        },
        {
            'city': 'Владивосток',
            'phone': '+7-999-999-9999',
            'email': 'info_vladivostok@interiorshop.ru',
            'address': 'Близко к океану',
        },
    ]

    content = {'title': title, 'visit_date': visit_date, 'locations': locations}
    return render(request, 'contact.html',  content)
# Create your views here.

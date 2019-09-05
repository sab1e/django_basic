from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Sum
import datetime
from .models import ProductCategory, Product
from basketapp.models import Basket


def main(request):
    title = 'Main'

    products = Product.objects.all()

    content = {'title': title, 'products': products}
    return render(request, 'index.html', content)


def products(request, pk=None):
    title = 'Products'
    products_category = ProductCategory.objects.all()

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
        basket_count = basket.aggregate(Sum('quantity'))

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'ВСЕ'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        content = {
            'title': title,
            'products_category': products_category,
            'category': category,
            'products': products,
            'basket_count': basket_count
        }
        return render(request, 'products_list.html', content)

    products = Product.objects.all()

    content = {
        'title': title,
        'products_category': products_category,
        'products': products,
        'basket_count': basket_count
    }

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

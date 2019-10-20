from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ProductCategory, Product
from django.views.generic.list import ListView
import datetime
import random


def main(request):
    title = 'Main'

    products = Product.objects.all()

    content = {'title': title, 'products': products}
    return render(request, 'index.html', content)


class MainListView(ListView):
    model = Product
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главня'

        return context


def products(request, pk=None, page=1):
    title = 'Товары'
    products_category = ProductCategory.objects.filter(is_active=True)

    if pk is not None:
        if pk == 0:
            products = Product.objects.filter(is_active=True,
                  category__is_active=True).order_by('price')
            category = {
                'pk': 0,
                'name': 'ВСЕ'
            }
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk,
                    is_active=True, category__is_active=True).order_by('price')

        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': title,
            'products_category': products_category,
            'category': category,
            'products': products_paginator,
        }
        return render(request, 'products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': title,
        'products_category': products_category,
        'hot_product': hot_product,
        'same_products': same_products,
    }

    return render(request, 'products.html', content)


def product(request, pk):
    title = 'Товар'

    content = {
        'title': title,
        'products_category': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
    }

    return render(request, 'product.html', content)


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


def get_hot_product():
    products = Product.objects.all()

    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]

    return same_products

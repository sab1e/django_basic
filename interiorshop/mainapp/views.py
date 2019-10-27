from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django.conf import settings
from django.template.loader import render_to_string
from django.views.generic.list import ListView
from django.views.decorators.cache import cache_page
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection
from .models import ProductCategory, Product
import datetime
import random


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile{type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        instance.product_set.update(is_activate=True)
    else:
        instance.product_set.update(is_active=False)

    db_profile_by_type(sender, 'UPDATE', connection.queries)


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'products_category'
        products_category = cache.get(key)
        if products_category is None:
            products_category = ProductCategory.objects.filter(is_active=True)
            cache.set(key, products_category)
        return products_category
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True,
                                              category__is_active=True).select_related(
                'category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True,
                                      category__is_active=True).select_related(
            'category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True,
                                category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True,
                                category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True,
                              category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True,
                              category__is_active=True).order_by('price')


def get_hot_product():
    products = get_products()

    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(
        category=hot_product.category).exclude(pk=hot_product.pk)[:3]

    return same_products


def main(request):
    title = 'Main'

    products = get_products()[:3]

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
    products_category = get_links_menu()

    if pk:
        if pk == '0':
            products = get_products_orederd_by_price()
            category = {
                'pk': 0,
                'name': 'ВСЕ'
            }
        else:
            category = get_category(pk)
            products = get_products_in_category_orederd_by_price(pk)

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


def products_ajax(request, pk=None, page=1):
    if request.is_ajax():
        products_category = get_links_menu()

        if pk:
            if pk == '0':
                products = get_products_orederd_by_price()
                category = {
                    'pk': 0,
                    'name': 'ВСЕ'
                }
            else:
                category = get_category(pk)
                products = get_products_in_category_orederd_by_price(pk)

            paginator = Paginator(products, 2)
            try:
                products_paginator = paginator.page(page)
            except PageNotAnInteger:
                products_paginator = paginator.page(1)
            except EmptyPage:
                products_paginator = paginator.page(paginator.num_pages)

            content = {
                'products_category': products_category,
                'category': category,
                'products': products_paginator,
            }

            result = render_to_string(
                'includes/inc_products_list_content.html',
                context=content,
                request=request
            )

            return JsonResponse({'result': result})


def product(request, pk):
    title = 'Товар'
    products_category = get_links_menu()
    product = get_product(pk)

    content = {
        'title': title,
        'products_category': products_category,
        'product': product,
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

    content = {'title': title, 'visit_date': visit_date,
               'locations': locations}
    return render(request, 'contact.html', content)

from django.shortcuts import render
import datetime


def main(request):
    title = 'Main'
    main_links_menu = [
        {'href': 'main', 'name': 'home'},
        {'href': 'products', 'name': 'products'},
        {'href': 'contact', 'name': 'contact'},
    ]

    content = {'title': title, 'main_links_menu': main_links_menu}
    return render(request, 'index.html',  content)


def products(request):
    title = 'Products'

    main_links_menu = [
        {'href': 'main', 'name': 'home'},
        {'href': 'products', 'name': 'products'},
        {'href': 'contact', 'name': 'contact'},
    ]

    links_menu = [
        {'href': 'products_all', 'name': 'all'},
        {'href': 'products_home', 'name': 'home'},
        {'href': 'products_office', 'name': 'office'},
        {'href': 'products_furniture', 'name': 'furniture'},
        {'href': 'products_modern', 'name': 'modern'},
        {'href': 'products_classic', 'name': 'classic'},
    ]

    products = [
        {
            'name': 'Fishnet Chair',
            'desc': 'Seat and back with upholstery made of cold cure foam. Steel frame, available in matt powder-coated black or highly polished chrome.',
            'image_src': 'product-11.jpg',
            'alt': 'product 11'
        },
        {
            'name': 'Fishnet Chair',
            'desc': 'Seat and back with upholstery made of cold cure foam. Steel frame, available in matt powder-coated black or highly polished chrome.',
            'image_src': 'product-21.jpg',
            'alt': 'product 21'
        },
        {
            'name': 'Fishnet Chair',
            'desc': 'Seat and back with upholstery made of cold cure foam. Steel frame, available in matt powder-coated black or highly polished chrome.',
            'image_src': 'product-31.jpg',
            'alt': 'product 31'
        },
        {
            'name': 'Fishnet Chair',
            'desc': 'Seat and back with upholstery made of cold cure foam. Steel frame, available in matt powder-coated black or highly polished chrome.',
            'image_src': 'product-41.jpg',
            'alt': 'product 41'
        },
        {
            'name': 'Fishnet Chair',
            'desc': 'Seat and back with upholstery made of cold cure foam. Steel frame, available in matt powder-coated black or highly polished chrome.',
            'image_src': 'product-5.jpg',
            'alt': 'product 5'
        },
        {
            'name': 'Fishnet Chair',
            'desc': 'Seat and back with upholstery made of cold cure foam. Steel frame, available in matt powder-coated black or highly polished chrome.',
            'image_src': 'product-6.jpg',
            'alt': 'product 6'
        },
    ]

    content = {'title': title, 'links_menu': links_menu, 'main_links_menu': main_links_menu, 'products': products}
    return render(request, 'products.html', content)


def contact(request):
    title = 'Contact'

    main_links_menu = [
        {'href': 'main', 'name': 'home'},
        {'href': 'products', 'name': 'products'},
        {'href': 'contact', 'name': 'contact'},
    ]

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

    content = {'title': title, 'main_links_menu': main_links_menu, 'visit_date': visit_date, 'locations': locations}
    return render(request, 'contact.html',  content)
# Create your views here.

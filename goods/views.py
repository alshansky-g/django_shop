from django.shortcuts import render

from goods.models import Product


def catalog(request, category_slug):
    if category_slug == 'all':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category__slug=category_slug)
    context = {
        'title': 'Home - Каталог',
        'products': products
    }
    return render(request, 'goods/catalog.html', context=context)


def product(request, product_slug: str):
    product = Product.objects.get(slug=product_slug)
    context = {
        'product': product
    }
    return render(request, 'goods/product.html', context=context)

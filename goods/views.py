from django.shortcuts import render

from goods.models import Product


def catalog(request):
    context = {
        'title': 'Home - Каталог',
    }
    return render(request, 'goods/catalog.html', context=context)


def product(request, product_slug: str):
    product = Product.objects.get(slug=product_slug)
    context = {
        'product': product
    }
    return render(request, 'goods/product.html', context=context)

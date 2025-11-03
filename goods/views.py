from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, render

from goods.models import Product


def catalog(request, category_slug: str):
    page = request.GET.get('page', 1)
    if category_slug == 'all':
        products = Product.objects.all()
    else:
        products = get_list_or_404(Product.objects.filter(category__slug=category_slug))
    paginator = Paginator(products, 3)
    current_page = paginator.get_page(page)
    context = {
        'title': 'Home - Каталог',
        'products': current_page,
        'slug_url': category_slug,
    }
    return render(request, 'goods/catalog.html', context=context)


def product(request, product_slug: str):
    product = Product.objects.get(slug=product_slug)
    context = {'product': product}
    return render(request, 'goods/product.html', context=context)

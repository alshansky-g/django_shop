from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, render

from goods.models import Product
from goods.utils import q_search


def catalog(request, category_slug: str | None = None):
    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)

    if category_slug == 'all':
        products = Product.objects.all()
    elif query:
        products = q_search(query)
    else:
        products = Product.objects.filter(category__slug=category_slug)

    if on_sale:
        products = products.filter(discount__gt=0)
    if order_by and order_by != 'default':
        products = products.order_by(order_by)

    products = get_list_or_404(products)

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

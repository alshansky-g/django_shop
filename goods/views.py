from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, render
from django.views.generic import DetailView, ListView

from goods.models import Product
from goods.utils import q_search


class CatalogView(ListView):
    model = Product
    template_name = 'goods/catalog.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        on_sale = self.request.GET.get('on_sale', None)
        order_by = self.request.GET.get('order_by', None)
        query = self.request.GET.get('q', None)

        if category_slug == 'all':
            products = super().get_queryset()
        elif query:
            products = q_search(query)
        else:
            products = super().get_queryset().filter(category__slug=category_slug)

        if on_sale:
            products = products.filter(discount__gt=0)
        if order_by and order_by != 'default':
            products = products.order_by(order_by)

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Home - Каталог',
            'slug_url': self.kwargs.get('category_slug'),
        })
        return context


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


class ProductView(DetailView):
    template_name = 'goods/product.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': self.object.name})
        return context

    def get_object(self) -> Product:
        product = Product.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product

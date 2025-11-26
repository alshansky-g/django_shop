from django.views.generic import DetailView, ListView

from goods.models import Product
from goods.utils import q_search


class CatalogView(ListView):
    model = Product
    template_name = 'goods/catalog.html'
    queryset = Product.objects.filter(quantity__gt=0)
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
            'total_products': context['page_obj'].paginator.count,
        })
        return context


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

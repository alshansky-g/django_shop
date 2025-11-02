from django import template

from goods.models import Category, Product

register = template.Library()


@register.simple_tag()
def tag_categories():
    return Category.objects.all()


@register.simple_tag()
def tag_products():
    return Product.objects.all()

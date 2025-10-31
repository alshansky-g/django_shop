from django.shortcuts import render


def catalog(request):
    return render(request, 'goods/catalog.html', {'title': 'Все товары'})


def product(request):
    return render(request, 'goods/product.html')

from django.shortcuts import render

from goods.models import Category


def index(request):
    categories = Category.objects.all()
    context = {
        'title': "Home - Главная",
        'content': 'Магазин мебели HOME',
        'categories': categories,
    }
    return render(request, 'main/index.html', context=context)


def about(request):
    context = {
        'title': 'Home - О нас',
        'content': "О нас",
        'text_on_page': 'Тут информация о нас, наших ценностях и миссии.'
    }
    return render(request, 'main/about.html', context=context)

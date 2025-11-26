from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Home - Главная',
            'content': 'Магазин мебели HOME',
        })
        return context


class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Home - О нас',
            'content': 'О нас',
            'text_on_page': 'Тут информация о нас, наших ценностях и миссии.',
        })
        return context

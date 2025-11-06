from django.db.models import Q

from goods.models import Product

MAX_ID_LENGTH = 5
STOP_WORDS_LENGTH = 3


def q_search(query):
    if query.isdigit() and len(query) <= MAX_ID_LENGTH:
        return Product.objects.filter(id=int(query))

    keywords = [word for word in query.split() if len(word) > STOP_WORDS_LENGTH]
    q_objects = Q()
    for token in keywords:
        q_objects |= Q(description__icontains=token)
        q_objects |= Q(name__icontains=token)

    return Product.objects.filter(q_objects)

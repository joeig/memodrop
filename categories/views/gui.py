import random

from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from cards.models import Card
from categories.models import Category


class CategoryList(ListView):
    """List all categories
    """
    model = Category
    paginate_by = 25
    paginate_orphans = 5


class CategoryDetail(DetailView):
    """Show detailed information about a category
    """
    model = Category

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        context['area1'] = Card.objects.filter(category_id=self.object.id, _area=1).all()
        context['area2'] = Card.objects.filter(category_id=self.object.id, _area=2).all()
        context['area3'] = Card.objects.filter(category_id=self.object.id, _area=3).all()
        context['area4'] = Card.objects.filter(category_id=self.object.id, _area=4).all()
        context['area5'] = Card.objects.filter(category_id=self.object.id, _area=5).all()
        context['area6'] = Card.objects.filter(category_id=self.object.id, _area=6).all()
        return context


class CategoryCreate(CreateView):
    """Create a new category
    """
    model = Category
    fields = ['name', 'description', 'mode']
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        messages.success(self.request, 'Category created.')
        return super(CategoryCreate, self).form_valid(form)


class CategoryUpdate(UpdateView):
    """Update a category
    """
    model = Category
    fields = ['name', 'description', 'mode']
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        messages.success(self.request, 'Category updated.')
        return super(CategoryUpdate, self).form_valid(form)


class CategoryDelete(DeleteView):
    model = Category
    success_url = reverse_lazy('category-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Category deleted.')
        return super(CategoryDelete, self).delete(request, *args, **kwargs)


def braindump_index(request):
    """List all possible Braindump sessions
    """
    category_list = Category.objects.all()

    context = {
        'category_list': category_list,
    }

    return render(request, 'braindump/braindump_index.html', context)


def braindump_session(request, category_pk):
    """Run a Braindump session for all cards in a certain category
    """

    min_area, max_area = braindump_validate_min_max_area(request)

    # Handle query string:
    query_string = braindump_generate_min_max_area_query_string(min_area, max_area)
    if query_string:
        query_string = '?{}'.format(query_string)

    # order_by('?') returns *one* random Card object
    # Maybe a better choice: https://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python/

    # Query the desired cards:
    cards = Card.objects.filter(
        category_id=category_pk,
        _area__gte=min_area,
        _area__lte=max_area,
    ).all()

    # Sort the cards by occurrence:
    try:
        distributed_cards = list()
        for area in range(min_area, max_area + 1):
            area_cards = list(cards.filter(_area=area))
            distributed_cards += area_cards * int(10 / area)

        card = random.choice(distributed_cards)

        context = {
            'card': card,
            'braindump_ok_query_string': query_string,
            'braindump_nok_query_string': query_string,
            'braindump_try_again_query_string': query_string,
        }

        return render(request, 'braindump/braindump_session.html', context)
    except IndexError:
        messages.warning(request, 'Cannot find any cards for this category in the desired areas.')
        return redirect(request.META.get('HTTP_REFERER', reverse('braindump-index')))


def braindump_ok(request, card_pk, category_pk):
    """Handle clicks on the "OK" button in Braindump
    """
    card = Card.objects.get(id=card_pk)
    card.move_forward()

    min_area, max_area = braindump_validate_min_max_area(request)

    # Handle query string:
    query_string = braindump_generate_min_max_area_query_string(min_area, max_area)
    if query_string:
        query_string = '?{}'.format(query_string)

    return redirect('{}{}'.format(reverse('braindump-session', args=(category_pk,)), query_string))


def braindump_nok(request, card_pk, category_pk):
    """Handle clicks on the "Not OK" button on Braindump
    """
    card = Card.objects.get(id=card_pk)
    category = Category.objects.get(id=category_pk)

    if category.mode == 1:
        card.reset()
    elif category.mode == 2:
        card.move_backward()

    min_area, max_area = braindump_validate_min_max_area(request)

    # Handle query string:
    query_string = braindump_generate_min_max_area_query_string(min_area, max_area)
    if query_string:
        query_string = '?{}'.format(query_string)

    return redirect('{}{}'.format(reverse('braindump-session', args=(category_pk,)), query_string))


def braindump_validate_min_max_area(request):
    """Validate min_area and max_area query string attributes
    """
    # Validate the min area:
    min_area = int(request.GET.get('min_area', 1))
    if not 1 <= min_area <= 6:
        messages.error(request, 'The first area is area 1.')
        return redirect(request.META.get('HTTP_REFERER', reverse('braindump-index')))

    # Validate the max area:
    max_area = int(request.GET.get('max_area', 6))
    if not 1 <= max_area <= 6:
        messages.error(request, 'The last area is area 6.')
        return redirect(request.META.get('HTTP_REFERER', reverse('braindump-index')))

    if max_area < min_area:
        messages.error(request, 'The max area cannot be lower than the min area.')
        return redirect(request.META.get('HTTP_REFERER', reverse('braindump-index')))

    return min_area, max_area


def braindump_generate_min_max_area_query_string(min_area=1, max_area=6):
    """Build a query string containing min_area and max_area
    """
    query_string = dict()

    if min_area != 1:
        query_string['min_area'] = min_area

    if max_area != 6:
        query_string['max_area'] = max_area

    return '&'.join('{}={}'.format(key, value) for key, value in query_string.items())

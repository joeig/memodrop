import random

from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from cards.models import Card
from .models import Category


class CategoryList(ListView):
    model = Category
    paginate_by = 25
    paginate_orphans = 5


class CategoryDetail(DetailView):
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
    model = Category
    fields = ['name', 'description']
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        messages.success(self.request, 'Category created.')
        return super(CategoryCreate, self).form_valid(form)


class CategoryUpdate(UpdateView):
    model = Category
    fields = ['name', 'description']
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
    category_list = Category.objects.all()

    context = {
        'category_list': category_list,
    }

    return render(request, 'braindump_index.html', context)


def braindump_session(request, category_pk):
    # order_by('?') returns *one* random Card object
    # Maybe a better choice: https://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python/

    cards = Card.objects.filter(
        category_id=category_pk,
    ).all()

    distributed_cards = list()
    for area in range(1, 7):
        area_cards = list(cards.filter(_area=area))
        distributed_cards += area_cards * int(10 / area)

    card = random.choice(distributed_cards)

    if card:
        context = {
            'card': card,
        }

        return render(request, 'braindump_session.html', context)
    else:
        messages.warning(request, 'Cannot find any cards for this category.')
        return redirect(request.META.get('HTTP_REFERER', reverse('braindump-index')))


def braindump_ok(request, card_pk, category_pk):
    card = Card.objects.get(id=card_pk)
    card.move_forward()

    return redirect('braindump-session', category_pk=category_pk)


def braindump_nok(request, card_pk, category_pk):
    card = Card.objects.get(id=card_pk)
    card.reset()

    return redirect('braindump-session', category_pk=category_pk)

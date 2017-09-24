from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category
from cards.models import Card


class CategoryList(ListView):
    model = Category


class CategoryDetail(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        context['area1'] = Card.objects.filter(category_id=self.object.id, area=1).all()
        context['area2'] = Card.objects.filter(category_id=self.object.id, area=2).all()
        context['area3'] = Card.objects.filter(category_id=self.object.id, area=3).all()
        context['area4'] = Card.objects.filter(category_id=self.object.id, area=4).all()
        context['area5'] = Card.objects.filter(category_id=self.object.id, area=5).all()
        context['area6'] = Card.objects.filter(category_id=self.object.id, area=6).all()
        return context


class CategoryCreate(CreateView):
    model = Category
    fields = ['name', 'description']


class CategoryUpdate(UpdateView):
    model = Category
    fields = ['name', 'description']


class CategoryDelete(DeleteView):
    model = Category
    success_url = reverse_lazy('category-list')


def braindump_index(request):
    category_list = Category.objects.all()

    context = {
        'category_list': category_list,
    }

    return render(request, 'braindump_index.html', context)


def braindump_session(request, category_pk):
    # order_by('?') returns a random Card object
    card = Card.objects.filter(
        category_id=category_pk,
        area__lt=6
    ).order_by('?').first()

    if not card:
        messages.warning(request, 'There are no more cards in area 1-5.')

        # order_by('?') returns a random Card object
        card = Card.objects.filter(
            category_id=category_pk
        ).order_by('?').first()

    if card:
        context = {
            'card': card,
        }

        return render(request, 'braindump_session.html', context)
    else:
        messages.warning(request, 'There are also no cards in area 6.')
        return redirect(request.META.get('HTTP_REFERER'))


def braindump_ok(request, card_pk, category_pk):
    card = Card.objects.get(id=card_pk)
    card.move_forward()

    return redirect('braindump-session', category_pk=category_pk)


def braindump_nok(request, card_pk, category_pk):
    card = Card.objects.get(id=card_pk)
    card.reset()

    return redirect('braindump-session', category_pk=category_pk)

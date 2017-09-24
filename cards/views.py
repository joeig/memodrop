from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Card


class CardList(ListView):
    model = Card


class CardDetail(DetailView):
    model = Card


class CardCreate(CreateView):
    model = Card
    fields = ['question',
              'answer',
              'hint',
              'area',
              'category']

    def form_valid(self, form):
        if self.request.POST.get('save') == 'Save and create another':
            form.save()
            return redirect('card-create')
        else:
            return super(CardCreate, self).form_valid(form)


class CardUpdate(UpdateView):
    model = Card
    fields = ['question',
              'answer',
              'hint',
              'area',
              'category']

    def form_valid(self, form):
        if self.request.POST.get('save') == 'Save and create another':
            form.save()
            return redirect('card-create')
        else:
            return super(CardUpdate, self).form_valid(form)


class CardDelete(DeleteView):
    model = Card
    success_url = reverse_lazy('card-list')


def card_reset(request, pk):
    card = Card.objects.get(id=pk)
    card.reset()

    messages.success(request, 'Card #{} was moved to area 1.'.format(card.pk))

    return redirect(request.META.get('HTTP_REFERER'))

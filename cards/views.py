from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

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

    def get_initial(self):
        # Pre-select desired category:
        return {
            'category': self.request.GET.get('category')
        }

    def form_valid(self, form):
        messages.success(self.request, 'Created card in category "{}".'.format(form.cleaned_data.get('category')))

        if self.request.POST.get('save') == 'Save and Create New':
            form.save()
            # Pre-select last category:
            query_string = '?category={}'.format(form.cleaned_data.get('category').id)
            return HttpResponseRedirect(reverse('card-create') + query_string)
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
        messages.success(self.request, 'Updated card in category "{}".'.format(form.cleaned_data.get('category')))

        if self.request.POST.get('save') == 'Save and Create New':
            form.save()
            # Pre-select last category:
            query_string = '?category={}'.format(form.cleaned_data.get('category').id)
            return HttpResponseRedirect(reverse('card-create') + query_string)
        else:
            return super(CardUpdate, self).form_valid(form)


class CardDelete(DeleteView):
    model = Card
    success_url = reverse_lazy('card-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Card deleted.')
        return super(CardDelete, self).delete(request, *args, **kwargs)


def card_reset(request, pk):
    card = Card.objects.get(id=pk)
    prev_area = card.area

    if prev_area != 1:
        card.reset()
        messages.success(request, 'Card moved form area {} to area 1.'.format(prev_area))
    else:
        messages.success(request, 'Card is already in area 1.')

    return redirect(request.META.get('HTTP_REFERER'))

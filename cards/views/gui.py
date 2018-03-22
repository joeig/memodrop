from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.safestring import mark_safe
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from cards.models import Card
from categories.models import Category


class CardBelongsUserMixin:
    """Mixin that returns all cards belonging to the authorized user
    """
    def get_queryset(self):
        return Card.user_objects.all(self.request.user)


class CardList(LoginRequiredMixin, CardBelongsUserMixin, ListView):
    """List all cards
    """
    paginate_by = 25
    paginate_orphans = 5


class CardDetail(LoginRequiredMixin, CardBelongsUserMixin, DetailView):
    """Show detailed information about a card
    """
    pass


class CardCreate(LoginRequiredMixin, CardBelongsUserMixin, CreateView):
    """Create a new card
    """
    model = Card
    fields = ['question',
              'hint',
              'answer',
              'area',
              'category']
    template_name_suffix = '_create_form'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['category'].queryset = Category.user_objects.all(self.request.user)
        return form

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


class CardUpdate(LoginRequiredMixin, CardBelongsUserMixin, UpdateView):
    """Update a card
    """
    fields = ['question',
              'hint',
              'answer',
              'area',
              'category']
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        messages.success(self.request, 'Updated card in category "{}".'.format(form.cleaned_data.get('category')))

        if self.request.POST.get('save') == 'Save and Create New':
            form.save()
            # Pre-select last category:
            query_string = '?category={}'.format(form.cleaned_data.get('category').id)
            return HttpResponseRedirect(reverse('card-create') + query_string)
        else:
            return super(CardUpdate, self).form_valid(form)


class CardDelete(LoginRequiredMixin, CardBelongsUserMixin, DeleteView):
    """Delete a card
    """
    success_url = reverse_lazy('card-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Card deleted.')
        return super(CardDelete, self).delete(request, *args, **kwargs)


@login_required
def card_reset(request, pk):
    """Handle clicks on the "Reset" button of a card
    """
    card = Card.user_objects.get(request.user, id=pk)
    prev_area = card.area

    if prev_area != 1:
        card.reset()
        undo_url = reverse('card-set-area', args=(card.pk, prev_area))
        messages.success(
            request,
            mark_safe('Card moved from area {} to area 1. <a href="{}">Undo</a>'.format(prev_area, undo_url))
        )
    else:
        messages.success(request, 'Card is already in area 1.')

    return redirect(request.META.get('HTTP_REFERER', reverse('card-detail', args=(card.pk,))))


@login_required
def card_set_area(request, pk, area):
    """Handle manual movements of a card
    """
    card = Card.user_objects.get(request.user, id=pk)
    prev_area = card.area
    card.area = area
    card.save()
    messages.success(request, 'Card moved from area {} to area {}.'.format(prev_area, card.area))

    return redirect(request.META.get('HTTP_REFERER', reverse('card-detail', args=(card.pk,))))

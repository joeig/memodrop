from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.safestring import mark_safe
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from braindump.models import CardPlacement
from cards.models import Card
from categories.models import Category


class CardBelongsOwnerMixin:
    """Mixin that returns all cards owned by the authorized user
    """
    def get_queryset(self):
        return Card.owned_objects.all(self.request.user)


class CardBelongsUserMixin:
    """Mixin that returns all cards belonging to the authorized user
    """
    def get_queryset(self):
        owned_card_list = Card.owned_objects.all(self.request.user)
        shared_card_list = Card.shared_objects.all(self.request.user)
        return owned_card_list | shared_card_list


class CardList(LoginRequiredMixin, CardBelongsUserMixin, ListView):
    """List all cards
    """
    paginate_by = 25
    paginate_orphans = 5
    template_name = 'cards/card_list.html'

    def get_queryset(self):
        return CardPlacement.user_objects.all(self.request.user)


class CardDetail(LoginRequiredMixin, CardBelongsUserMixin, DetailView):
    """Show detailed information about a card
    """
    def get_context_data(self, **kwargs):
        context = super(CardDetail, self).get_context_data(**kwargs)
        context['card_placement'] = CardPlacement.card_user_objects.get(self.object, self.request.user)
        return context


class CardCreate(LoginRequiredMixin, CardBelongsUserMixin, CreateView):
    """Create a new card
    """
    model = Card
    fields = ['question',
              'hint',
              'answer',
              'category']
    template_name_suffix = '_create_form'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['question'].help_text = 'You can use Markdown.'
        form.fields['hint'].help_text = 'You can use Markdown.'
        form.fields['answer'].help_text = 'You can use Markdown.'
        form.fields['category'].queryset = Category.owned_objects.all(self.request.user) | \
            Category.shared_objects.all(self.request.user)
        return form

    def get_initial(self):
        # Pre-select desired category:
        return {
            'category': self.request.GET.get('category')
        }

    def form_valid(self, form):
        if self.request.POST.get('save') == 'Save and create new':
            card_object = form.save()

            # Pre-select last category:
            query_string = '?category={}'.format(card_object.category.pk)
            resp = HttpResponseRedirect(reverse('card-create') + query_string)

            messages.success(
                self.request,
                mark_safe(
                    'Created <a href="{}">{}</a> in category <a href="{}">"{}"</a>.'.format(
                        reverse('card-detail', args=(card_object.pk,)),
                        card_object,
                        reverse('category-detail', args=(card_object.category.pk,)),
                        card_object.category,
                    )
                )
            )
        else:
            resp = super(CardCreate, self).form_valid(form)

            messages.success(
                self.request,
                mark_safe(
                    'Created <a href="{}">{}</a> in category <a href="{}">"{}"</a>. '
                    '<a href="{}">Create New</a>'.format(
                        reverse('card-detail', args=(self.object.pk,)),
                        self.object,
                        reverse('category-detail', args=(self.object.category.pk,)),
                        self.object.category,
                        reverse('card-create') + '?category={}'.format(self.object.category.pk),
                    )
                )
            )

        return resp


class CardUpdate(LoginRequiredMixin, CardBelongsUserMixin, UpdateView):
    """Update a card
    """
    fields = ['question',
              'hint',
              'answer']
    template_name_suffix = '_update_form'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['question'].help_text = 'You can use Markdown.'
        form.fields['hint'].help_text = 'You can use Markdown.'
        form.fields['answer'].help_text = 'You can use Markdown.'
        return form

    def form_valid(self, form):
        if self.request.POST.get('save') == 'Save and Create New':
            card_object = form.save()

            # Pre-select last category:
            query_string = '?category={}'.format(card_object.category.pk)
            resp = HttpResponseRedirect(reverse('card-create') + query_string)

            messages.success(
                self.request,
                mark_safe(
                    'Updated <a href="{}">{}</a> in category <a href="{}">"{}"</a>. '.format(
                        reverse('card-detail', args=(card_object.pk,)),
                        card_object,
                        reverse('category-detail', args=(card_object.category.pk,)),
                        card_object.category,
                    )
                )
            )
        else:
            resp = super(CardUpdate, self).form_valid(form)

            messages.success(
                self.request,
                mark_safe(
                    'Updated <a href="{}">{}</a> in category <a href="{}">"{}"</a>. '
                    '<a href="{}">Create New</a>'.format(
                        reverse('card-detail', args=(self.object.pk,)),
                        self.object,
                        reverse('category-detail', args=(self.object.category.pk,)),
                        self.object.category,
                        reverse('card-create') + '?category={}'.format(self.object.category.pk),
                    )
                )
            )

        return resp


class CardDelete(LoginRequiredMixin, CardBelongsOwnerMixin, DeleteView):
    """Delete a card
    """
    success_url = reverse_lazy('card-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Card deleted.')
        return super(CardDelete, self).delete(request, *args, **kwargs)

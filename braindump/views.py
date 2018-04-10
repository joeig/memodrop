from datetime import timedelta

import numpy
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView, View, RedirectView

from braindump.models import CardPlacement
from categories.models import Category


class BraindumpViewMixin:
    """Mixin for Braindump views
    """
    def handle_query_string(self, request):
        """Handle query string
        """
        min_area, max_area = self.validate_min_max_area(request)
        query_string = self.generate_min_max_area_query_string(min_area, max_area)
        if query_string:
            query_string = '?{}'.format(query_string)

        return query_string

    def validate_min_max_area(self, request):
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

    def generate_min_max_area_query_string(self, min_area=1, max_area=6):
        """Build a query string containing min_area and max_area
        """
        query_string = dict()

        if min_area != 1:
            query_string['min_area'] = min_area

        if max_area != 6:
            query_string['max_area'] = max_area

        return '&'.join('{}={}'.format(key, value) for key, value in query_string.items())

    def get_probability_weighted_area(self, min_area=1, max_area=6):
        """Generate a random area by probability
        """
        # Generate range of selected areas:
        area_range = numpy.arange(min_area, max_area + 1)

        # Generate probability:
        area_probability = list()
        for _ in range(len(area_range)):
            area_probability.append(1 / 2 ** _)

        # Normalization of the probability:
        area_probability = numpy.array(area_probability)
        area_probability /= area_probability.sum()

        return numpy.random.choice(area_range, 1, p=area_probability)[0]


class BraindumpIndex(LoginRequiredMixin, TemplateView):
    """List all possible Braindump sessions
    """
    template_name = 'braindump/braindump_index.html'

    def get_context_data(self):
        category_list = Category.user_objects.all(self.request.user).order_by('last_interaction').reverse().all()

        context = {
            'category_list': category_list,
        }

        return context


class BraindumpSession(LoginRequiredMixin, View, BraindumpViewMixin):
    """Run a Braindump session for all cards in a certain category
    """
    http_method_names = ['get']

    def get(self, request, category_pk):
        get_object_or_404(Category.user_objects.all(self.request.user), pk=category_pk)
        query_string = self.handle_query_string(request)

        # Maybe a better choice: https://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python/

        min_area, max_area = self.validate_min_max_area(request)

        # Correct min/max area for getting only options with actually existing cards
        # (this does not exclude areas *between* min_area and max_area!):
        card_placement_filter = CardPlacement.user_objects.all(self.request.user).filter(
            card__category_id=category_pk,
            area__gte=min_area,
            area__lte=max_area,
            postpone_until__lte=timezone.now(),
        ).order_by('area')

        if card_placement_filter.exists():
            adjusted_min_area = card_placement_filter.first().area
            adjusted_max_area = card_placement_filter.last().area

            # If no card matches the selected area, retry:
            card_placement = False
            retries = 0
            while not card_placement and retries < 10:
                # Select an area:
                randomly_selected_area = self.get_probability_weighted_area(adjusted_min_area, adjusted_max_area)

                # Query a random card of the selected area (order_by('?') returns *one* random Card object):
                card_placement = CardPlacement.user_objects.all(self.request.user).filter(
                    card__category_id=category_pk,
                    area=randomly_selected_area,
                    postpone_until__lte=timezone.now(),
                ).order_by('?').first()

                retries += 1

            if card_placement:
                # Render a Braindump session containing the selected card:
                context = {
                    'card': card_placement.card,
                    'card_placement': card_placement,
                    'braindump_ok_query_string': query_string,
                    'braindump_nok_query_string': query_string,
                    'braindump_try_again_query_string': query_string,
                }

                return render(request, 'braindump/braindump_session.html', context)
            else:
                card_error = True
        else:
            card_error = True

        if card_error:
            messages.warning(
                request,
                'Cannot find any cards for this category in the desired areas. '
                'Is it possible that you postponed all possible cards?'
            )
            return redirect(reverse('braindump-index'))


class BraindumpOK(LoginRequiredMixin, RedirectView, BraindumpViewMixin):
    """Handle clicks on the "OK" button
    """
    permanent = False

    def get_redirect_url(self, card_pk, category_pk):
        card_placement = get_object_or_404(CardPlacement.user_objects.all(self.request.user), card_id=card_pk)
        card_placement.move_forward()
        card_placement.set_last_interaction()
        card_placement.card.category.set_last_interaction()

        query_string = self.handle_query_string(self.request)

        return '{}{}'.format(reverse('braindump-session', args=(category_pk,)), query_string)


class BraindumpNOK(LoginRequiredMixin, RedirectView, BraindumpViewMixin):
    """Handle clicks on the "Not OK" button
    """
    permanent = False

    def get_redirect_url(self, card_pk, category_pk):
        card_placement = get_object_or_404(CardPlacement.user_objects.all(self.request.user), card_id=card_pk)

        if card_placement.card.category.mode == 1:
            card_placement.reset()
        elif card_placement.card.category.mode == 2:
            card_placement.move_backward()

        card_placement.set_last_interaction()
        card_placement.card.category.set_last_interaction()

        query_string = self.handle_query_string(self.request)

        return '{}{}'.format(reverse('braindump-session', args=(category_pk,)), query_string)


class BraindumpPostpone(LoginRequiredMixin, RedirectView, BraindumpViewMixin):
    """Handle clicks on the "Postpone" button
    """
    permanent = False

    def get_redirect_url(self, card_pk, category_pk, seconds):
        card_placement = get_object_or_404(CardPlacement.user_objects.all(self.request.user), card_id=card_pk)

        if int(seconds) > settings.BRAINDUMP_MAX_POSTPONE_SECONDS:
            messages.error(
                self.request,
                'Cannot postpone a card for more than {} seconds.'.format(settings.BRAINDUMP_MAX_POSTPONE_SECONDS)
            )
        else:
            card_placement.postpone_until = timezone.now() + timedelta(seconds=int(seconds))
            messages.info(self.request, 'Ok, I will not show the card for 15 minutes from now.')

        card_placement.set_last_interaction()
        card_placement.card.category.set_last_interaction()

        query_string = self.handle_query_string(self.request)

        return '{}{}'.format(reverse('braindump-session', args=(category_pk,)), query_string)


class CardExpedite(LoginRequiredMixin, RedirectView, BraindumpViewMixin):
    """Expedite a card (undo postpone)
    """
    permanent = False

    def get_redirect_url(self, card_pk):
        card_placement = get_object_or_404(CardPlacement.user_objects.all(self.request.user), card_id=card_pk)
        card_placement.expedite()
        messages.success(
            self.request,
            mark_safe('The postpone marker of <a href="{}">{}</a> has been removed.'.format(
                reverse('card-detail', args=(card_placement.card.pk,)),
                card_placement.card
            ))
        )
        return self.request.META.get('HTTP_REFERER', reverse('card-detail', args=(card_placement.card.pk,)))


class CardReset(LoginRequiredMixin, RedirectView, BraindumpViewMixin):
    """Handle clicks on the "Reset" button of a card
    """
    permanent = False

    def get_redirect_url(self, card_pk):
        card_placement = get_object_or_404(CardPlacement.user_objects.all(self.request.user), card_id=card_pk)
        prev_area = card_placement.area

        if prev_area != 1:
            card_placement.reset()
            undo_url = reverse('card-set-area', args=(card_placement.pk, prev_area))
            messages.success(
                self.request,
                mark_safe('{} moved from area {} to area 1. <a href="{}">Undo</a>'.format(card_placement, prev_area,
                                                                                          undo_url))
            )
        else:
            messages.success(self.request, 'Card is already in area 1.')

        return self.request.META.get('HTTP_REFERER', reverse('card-detail', args=(card_placement.pk,)))


class CardSetArea(LoginRequiredMixin, RedirectView, BraindumpViewMixin):
    """Handle manual movements of a card
    """
    permanent = False

    def get_redirect_url(self, card_pk, area):
        card_placement = get_object_or_404(CardPlacement.user_objects.all(self.request.user), card_id=card_pk)
        prev_area = card_placement.area
        card_placement.area = area
        card_placement.save()
        messages.success(self.request, '{} moved from area {} to area {}.'.format(card_placement.card, prev_area,
                                                                                  card_placement.area))
        return self.request.META.get('HTTP_REFERER', reverse('card-detail', args=(card_placement.card.pk,)))

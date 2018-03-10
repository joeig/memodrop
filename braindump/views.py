import random

from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, View, RedirectView

from cards.models import Card
from categories.models import Category


class BraindumpIndex(TemplateView):
    """List all possible Braindump sessions
    """

    template_name = "braindump/braindump_index.html"

    def get_context_data(self):
        category_list = Category.objects.all()

        context = {
            'category_list': category_list,
        }

        return context


class BraindumpSession(View):
    """Run a Braindump session for all cards in a certain category
    """

    def get(self, request, category_pk):
        min_area, max_area = Braindump.braindump_validate_min_max_area(request)

        # Handle query string:
        query_string = Braindump.braindump_generate_min_max_area_query_string(min_area, max_area)
        if query_string:
            query_string = '?{}'.format(query_string)

        # order_by('?') returns *one* random Card object
        # Maybe a better choice: https://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python/

        # Query the desired cards:
        cards = Card.objects.filter(
            category_id=category_pk,
            area__gte=min_area,
            area__lte=max_area,
        ).all()

        # Sort the cards by occurrence:
        try:
            distributed_cards = list()
            for area in range(min_area, max_area + 1):
                area_cards = list(cards.filter(area=area))
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


class BraindumpOK(RedirectView):
    permanent = False

    def get_redirect_url(self, card_pk, category_pk):
        """Handle clicks on the "OK" button in Braindump
        """
        card = Card.objects.get(id=card_pk)
        card.move_forward()

        min_area, max_area = Braindump.braindump_validate_min_max_area(self.request)

        # Handle query string:
        query_string = Braindump.braindump_generate_min_max_area_query_string(min_area, max_area)
        if query_string:
            query_string = '?{}'.format(query_string)

        return '{}{}'.format(reverse('braindump-session', args=(category_pk,)), query_string)


class BraindumpNOK(RedirectView):
    """Handle clicks on the "Not OK" button on Braindump
    """

    def get_redirect_url(self, card_pk, category_pk):
        card = Card.objects.get(id=card_pk)
        category = Category.objects.get(id=category_pk)

        if category.mode == 1:
            card.reset()
        elif category.mode == 2:
            card.move_backward()

        min_area, max_area = Braindump.braindump_validate_min_max_area(self.request)

        # Handle query string:
        query_string = Braindump.braindump_generate_min_max_area_query_string(min_area, max_area)
        if query_string:
            query_string = '?{}'.format(query_string)

        return '{}{}'.format(reverse('braindump-session', args=(category_pk,)), query_string)


class Braindump:
    @staticmethod
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

    @staticmethod
    def braindump_generate_min_max_area_query_string(min_area=1, max_area=6):
        """Build a query string containing min_area and max_area
        """
        query_string = dict()

        if min_area != 1:
            query_string['min_area'] = min_area

        if max_area != 6:
            query_string['max_area'] = max_area

        return '&'.join('{}={}'.format(key, value) for key, value in query_string.items())

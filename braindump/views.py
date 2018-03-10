import numpy

from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404
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
        get_object_or_404(Category, pk=category_pk)

        # Maybe a better choice: https://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python/

        min_area, max_area = Braindump.braindump_validate_min_max_area(request)

        # Handle query string:
        query_string = Braindump.braindump_generate_min_max_area_query_string(min_area, max_area)
        if query_string:
            query_string = '?{}'.format(query_string)

        # Correct min/max area for getting only options with actually existing cards
        # (this does not exclude areas *between* min_area and max_area!):
        card_filter = Card.objects.filter(
            category_id=category_pk,
            area__gte=min_area,
            area__lte=max_area,
        ).order_by('area')
        adjusted_min_area = card_filter.first().area
        adjusted_max_area = card_filter.last().area

        # If no card matches the selected area, retry:
        card = False
        retries = 0
        while not card and retries < 10:
            # Select an area:
            randomly_selected_area = Braindump.get_probability_weighted_area(adjusted_min_area, adjusted_max_area)

            # Query a random card of the selected area (order_by('?') returns *one* random Card object):
            card = Card.objects.filter(
                category_id=category_pk,
                area=randomly_selected_area
            ).order_by('?').first()

            retries += 1

        if card:
            # Render a Braindump session containing the selected card:
            context = {
                'card': card,
                'braindump_ok_query_string': query_string,
                'braindump_nok_query_string': query_string,
                'braindump_try_again_query_string': query_string,
            }

            return render(request, 'braindump/braindump_session.html', context)
        else:
            messages.warning(request, 'Cannot find any cards for this category in the desired areas.')
            return redirect(request.META.get('HTTP_REFERER', reverse('braindump-index')))


class BraindumpOK(RedirectView):
    permanent = False

    def get_redirect_url(self, card_pk, category_pk):
        """Handle clicks on the "OK" button in Braindump
        """
        card = get_object_or_404(Card, pk=card_pk)
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
        card = get_object_or_404(Card, pk=card_pk)
        category = get_object_or_404(Category, pk=category_pk)

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

    @staticmethod
    def get_probability_weighted_area(min_area=1, max_area=6):
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

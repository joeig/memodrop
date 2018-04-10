import math
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from braindump.models import CardPlacement
from braindump.views import BraindumpViewMixin
from cards.models import Card
from categories.models import Category


class BraindumpTestCase(TestCase):
    test_cards = list()

    def setUp(self):
        """Set up test scenario
        """
        self.test_user = User.objects.create_user('test')
        self.test_category = Category.objects.create(name='Category 1', description='Description 1',
                                                     owner=self.test_user)
        self.client = Client()
        self.client.force_login(self.test_user)

        self.foreign_test_user = User.objects.create_user('foreigner')
        self.foreign_test_category = Category.objects.create(name='Category Foreign', description='Description Foreign',
                                                             owner=self.foreign_test_user)
        self.foreign_client = Client()
        self.foreign_client.force_login(self.foreign_test_user)
        self.foreign_test_card = Card.objects.create(
            question='Question Foreign',
            answer='Answer Foreign',
            hint='Hint Foreign',
            category=self.foreign_test_category,
        )

    def _create_test_card(self, suffix='', category=False, user=False):
        """Create a single test card
        """
        if not category:
            category = self.test_category
        if not user:
            user = self.test_user
        suffix = ' {}'.format(suffix)
        card = Card.objects.create(
            question='Question'.format(suffix),
            answer='Answer'.format(suffix),
            hint='Hint'.format(suffix),
            category=category,
        )
        card_placement = CardPlacement.card_user_objects.get(card, user)
        return card, card_placement

    def test_index(self):
        """Test if the braindump index is displayed successfully
        """
        url = reverse('braindump-index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_session(self):
        """Test if the braindump session starts successfully
        """
        test_card, test_card_placement = self._create_test_card()
        url = reverse('braindump-session', args=(test_card.category.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_unauth_braindump_session(self):
        """Test if the braindump session fails if the user is not allowed to access
        """
        test_card, test_card_placement = self._create_test_card(category=self.foreign_test_category,
                                                                user=self.foreign_test_user)
        url = reverse('braindump-session', args=(test_card.category.pk,))

        foreign_response = self.foreign_client.get(url)
        self.assertEqual(foreign_response.status_code, 200)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_ok(self):
        """Test if the "OK" button in braindump works
        """
        test_card, test_card_placement = self._create_test_card()
        url = reverse('braindump-ok', args=(test_card.category.pk, test_card.pk))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        refreshed_test_card_placement = CardPlacement.card_user_objects.get(card=test_card, user=self.test_user)
        self.assertEqual(refreshed_test_card_placement.area, 2)

    def test_strict_nok_on_area_3(self):
        """Test if the "OK" button in braindump works for cards in area 3 (strict mode)
        """
        test_category = Category.objects.create(name='Category 1337', description='Description 1337', mode=1,
                                                owner=self.test_user)
        test_card, test_card_placement = self._create_test_card(category=test_category)
        test_card_placement.area = 3
        test_card_placement.save()
        url = reverse('braindump-nok', args=(test_card.category.pk, test_card.pk))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        refreshed_test_card_placement = CardPlacement.card_user_objects.get(card=test_card, user=self.test_user)
        self.assertEqual(refreshed_test_card_placement.area, 1)

    def test_defensive_nok_on_area_3(self):
        """Test if the "Not OK" button in braindump works for cards in area 3 (defensive mode)
        """
        test_category = Category.objects.create(name='Category 1337', description='Description 1337', mode=2,
                                                owner=self.test_user)
        test_card, test_card_placement = self._create_test_card(category=test_category)
        test_card_placement.area = 3
        test_card_placement.save()
        url = reverse('braindump-nok', args=(test_card.category.pk, test_card.pk))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        refreshed_test_card_placement = CardPlacement.card_user_objects.get(card=test_card, user=self.test_user)
        self.assertEqual(refreshed_test_card_placement.area, 2)

    def test_strict_nok_on_area_1(self):
        """Test if the "Not OK" button in braindump works for cards in area 1 (strict mode)
        """
        test_category = Category.objects.create(name='Category 1337', description='Description 1337', mode=1,
                                                owner=self.test_user)
        test_card, test_card_placement = self._create_test_card(category=test_category)
        url = reverse('braindump-nok', args=(test_card.category.pk, test_card.pk))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        refreshed_test_card_placement = CardPlacement.card_user_objects.get(card=test_card, user=self.test_user)
        self.assertEqual(refreshed_test_card_placement.area, 1)

    def test_defensive_nok_on_area_1(self):
        """Test if the "Not OK" button in braindump works for cards in area 1 (defensive mode)
        """
        test_category = Category.objects.create(name='Category 1337', description='Description 1337', mode=2,
                                                owner=self.test_user)
        test_card, test_card_placement = self._create_test_card(category=test_category)
        url = reverse('braindump-nok', args=(test_card.category.pk, test_card.pk))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        refreshed_test_card_placement = CardPlacement.card_user_objects.get(card=test_card, user=self.test_user)
        self.assertEqual(refreshed_test_card_placement.area, 1)

    def test_postpone(self):
        """Test if the "Postpone" button works
        """
        test_card, test_card_placement = self._create_test_card()
        postpone_seconds = settings.BRAINDUMP_MAX_POSTPONE_SECONDS
        url = reverse('braindump-postpone', args=(test_card.category.pk, test_card.pk, postpone_seconds))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        refreshed_test_card_placement = CardPlacement.card_user_objects.get(card=test_card, user=self.test_user)
        self.assertGreater(refreshed_test_card_placement.postpone_until, timezone.now())

    def test_postpone_too_high(self):
        """Test if the "Postpone" button doesn't work if the value exceeds the configured setting
        """
        test_card, test_card_placement = self._create_test_card()
        postpone_seconds = settings.BRAINDUMP_MAX_POSTPONE_SECONDS + 1
        url = reverse('braindump-postpone', args=(test_card.category.pk, test_card.pk, postpone_seconds))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        refreshed_test_card_placement = CardPlacement.card_user_objects.get(card=test_card, user=self.test_user)
        self.assertEqual(refreshed_test_card_placement.postpone_until, test_card_placement.postpone_until)

    def test_validate_min_max_area_default(self):
        """Test if the default min_area and max_area query string attributes can be validated properly
        """
        class DummyRequest:
            GET = dict()

        bvm = BraindumpViewMixin()
        self.assertEqual(bvm.validate_min_max_area(DummyRequest), (1, 6))

    def test_validate_min_max_area_custom(self):
        """Test if custom min_area and max_area query string attributes can be validated properly
        """
        class DummyRequest:
            GET = {
                'min_area': 3,
                'max_area': 5,
            }

        bvm = BraindumpViewMixin()
        self.assertEqual(bvm.validate_min_max_area(DummyRequest), (3, 5))

    def test_generate_min_max_area_query_string_default(self):
        """Test if the query string for default min_area and max_area query string attributes can be generated properly
        """
        bvm = BraindumpViewMixin()
        self.assertEqual(bvm.generate_min_max_area_query_string(1, 6), '')

    def test_generate_min_max_area_query_string_custom(self):
        """Test if the query string for custom min_area and max_area query string attributes can be generated properly
        """
        bvm = BraindumpViewMixin()
        self.assertEqual(bvm.generate_min_max_area_query_string(2, 4), 'min_area=2&max_area=4')
        self.assertEqual(bvm.generate_min_max_area_query_string(2, 6), 'min_area=2')
        self.assertEqual(bvm.generate_min_max_area_query_string(1, 4), 'max_area=4')

    def test_probability_weighted_area(self):
        """Test if the probabilities are OK
        """
        # How many samples do you want to collect?
        cycles = 10000

        # Initialize occurrence counter:
        occurrences = dict()
        for _ in range(1, 7):
            occurrences[_] = 0

        # Collect samples:
        for _ in range(cycles):
            bvm = BraindumpViewMixin()
            sample = bvm.get_probability_weighted_area()
            occurrences[sample] += 1

        # Check occurrance share:
        for _ in range(1, 7):
            probability = 1 / 2 ** _
            share = occurrences[_] / cycles
            # Allow relative tolerance of 20 %:
            self.assertTrue(math.isclose(probability, share, rel_tol=0.2))

    def test_in_area_1(self):
        """Test if the new card is in area 1
        """
        test_card, test_card_placement = self._create_test_card()
        self.assertEqual(test_card_placement.area, 1)

    def test_move_forward(self):
        """Test if the card can be moved forward in the next area
        """
        test_card, test_card_placement = self._create_test_card()
        test_card_placement.area = 1
        test_card_placement.save()

        for i in range(2, 7):
            test_card_placement.move_forward()
            refreshed_test_card_placement = CardPlacement.card_user_objects.get(card=test_card, user=self.test_user)
            self.assertEqual(refreshed_test_card_placement.area, i)

    def test_move_too_much_forward(self):
        """Test if the card cannot be moved to area 7 which doesn't exist
        """
        test_card, test_card_placement = self._create_test_card()
        test_card_placement.area = 1
        test_card_placement.save()

        for i in range(2, 8):
            test_card_placement.move_forward()

        refreshed_test_card_placement = CardPlacement.card_user_objects.get(card=test_card, user=self.test_user)
        self.assertEqual(refreshed_test_card_placement.area, 6)

    def test_move_backward(self):
        """Test if the card can be moved backward in the next area
        """
        test_card, test_card_placement = self._create_test_card()
        test_card_placement.area = 6
        test_card_placement.save()

        for i in reversed(range(1, 6)):
            test_card_placement.move_backward()
            refreshed_test_card_placement = CardPlacement.card_user_objects.get(card=test_card, user=self.test_user)
            self.assertEqual(refreshed_test_card_placement.area, i)

    def test_move_too_much_backward(self):
        """Test if the card cannot be moved to area 0 which doesn't exist
        """
        test_card, test_card_placement = self._create_test_card()
        test_card_placement.area = 6
        test_card_placement.save()

        for _ in reversed(range(0, 6)):
            test_card_placement.move_backward()

        refreshed_test_card_placement = CardPlacement.card_user_objects.get(card=test_card, user=self.test_user)
        self.assertEqual(refreshed_test_card_placement.area, 1)

    def test_reset(self):
        """Test if the "Reset" button works
        """
        test_card, test_card_placement = self._create_test_card()
        test_card_placement.area = 3
        test_card_placement.save()

        url = reverse('card-reset', args=(test_card.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        refreshed_test_card_placement = CardPlacement.card_user_objects.get(card=test_card, user=self.test_user)
        self.assertEqual(refreshed_test_card_placement.area, 1)

    def test_expedite(self):
        """Test if the "Expedite" button works
        """
        test_card, test_card_placement = self._create_test_card()
        test_card_placement.postponed_until = timezone.now() + timedelta(
            seconds=settings.BRAINDUMP_MAX_POSTPONE_SECONDS
        )
        test_card_placement.save()

        url = reverse('card-expedite', args=(test_card.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        refreshed_test_card_placement = CardPlacement.card_user_objects.get(card=test_card, user=self.test_user)
        # Allow 1 second deviation:
        self.assertAlmostEqual(refreshed_test_card_placement.postpone_until, timezone.now(), delta=timedelta(seconds=1))

    def test_set_area_4(self):
        """Test if the card can be set to area 4
        """
        test_card, test_card_placement = self._create_test_card()
        test_card_placement.area = 2
        test_card_placement.save()

        url = reverse('card-set-area', args=(test_card.pk, 4))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        refreshed_test_card_placement = CardPlacement.card_user_objects.get(card=test_card, user=self.test_user)
        self.assertEqual(refreshed_test_card_placement.area, 4)

    def test_set_area_1337(self):
        """Test if the card cannot be set to area 1337
        """
        test_card, test_card_placement = self._create_test_card()
        test_card_placement.area = 4
        test_card_placement.save()

        # Set the URL manually instead of reverse(), because the URL regex wouldn't allow this test:
        url = '/card/{}/set-area/{}/'.format(test_card.pk, 1337)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        refreshed_test_card_placement = CardPlacement.card_user_objects.get(card=test_card, user=self.test_user)
        self.assertEqual(refreshed_test_card_placement.area, 4)

import math

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

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

        for i in range(1, 11):
            test_card = Card.objects.create(
                question='Question {}'.format(i),
                answer='Answer {}'.format(i),
                hint='Hint {}'.format(i),
                category=self.test_category,
            )
            self.test_cards.append(test_card)

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

    def test_braindump_index(self):
        """Test if the braindump index is displayed successfully
        """
        url = reverse('braindump-index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_braindump_session(self):
        """Test if the braindump session starts successfully
        """
        test_card = self.test_cards[0]
        url = reverse('braindump-session', args=(test_card.category.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_unauth_braindump_session(self):
        """Test if the braindump session fails if the user is not allowed to access
        """
        url = reverse('braindump-session', args=(self.foreign_test_card.category.pk,))

        foreign_response = self.foreign_client.get(url)
        self.assertEqual(foreign_response.status_code, 200)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_braindump_ok(self):
        """Test if the "OK" button in braindump works
        """
        test_card = self.test_cards[0]
        url = reverse('braindump-ok', args=(test_card.category.pk, test_card.pk))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        refreshed_test_card = Card.objects.get(pk=test_card.pk)
        self.assertEqual(refreshed_test_card.area, 2)

    def test_braindump_strict_nok_on_area_3(self):
        """Test if the "OK" button in braindump works for cards in area 3 (strict mode)
        """
        test_category = Category.objects.create(name='Category 1337', description='Description 1337', mode=1,
                                                owner=self.test_user)
        test_card = Card.objects.create(
            question='Question 1337',
            answer='Answer 1337',
            hint='Hint 1337',
            category=test_category,
            area=3,
        )
        url = reverse('braindump-nok', args=(test_card.category.pk, test_card.pk))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        refreshed_test_card = Card.objects.get(pk=test_card.pk)
        self.assertEqual(refreshed_test_card.area, 1)

    def test_braindump_defensive_nok_on_area_3(self):
        """Test if the "OK" button in braindump works for cards in area 3 (defensive mode)
        """
        test_category = Category.objects.create(name='Category 1337', description='Description 1337', mode=2,
                                                owner=self.test_user)
        test_card = Card.objects.create(
            question='Question 1337',
            answer='Answer 1337',
            hint='Hint 1337',
            category=test_category,
            area=3,
        )
        url = reverse('braindump-nok', args=(test_card.category.pk, test_card.pk))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        refreshed_test_card = Card.objects.get(pk=test_card.pk)
        self.assertEqual(refreshed_test_card.area, 2)

    def test_braindump_strict_nok_on_area_1(self):
        """Test if the "Not OK" button in braindump works for cards in area 1 (strict mode)
        """
        test_category = Category.objects.create(name='Category 1337', description='Description 1337', mode=1,
                                                owner=self.test_user)
        test_card = Card.objects.create(
            question='Question 1337',
            answer='Answer 1337',
            hint='Hint 1337',
            category=test_category,
            area=1,
        )
        url = reverse('braindump-nok', args=(test_card.category.pk, test_card.pk))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        refreshed_test_card = Card.objects.get(pk=test_card.pk)
        self.assertEqual(refreshed_test_card.area, 1)

    def test_braindump_defensive_nok_on_area_1(self):
        """Test if the "Not OK" button in braindump works for cards in area 3 (defensive mode)
        """
        test_category = Category.objects.create(name='Category 1337', description='Description 1337', mode=2,
                                                owner=self.test_user)
        test_card = Card.objects.create(
            question='Question 1337',
            answer='Answer 1337',
            hint='Hint 1337',
            category=test_category,
            area=1,
        )
        url = reverse('braindump-nok', args=(test_card.category.pk, test_card.pk))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        refreshed_test_card = Card.objects.get(pk=test_card.pk)
        self.assertEqual(refreshed_test_card.area, 1)

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

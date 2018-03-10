from django.test import TestCase, Client
from django.urls import reverse

from cards.models import Card
from categories.models import Category
from braindump.views import Braindump


class CardTestCase(TestCase):
    test_cards = list()

    def setUp(self):
        """Set up test scenario
        """
        self.client = Client()
        test_category = Category.objects.create(name='Category 1', description='Description 1')

        for i in range(1, 11):
            test_card = Card.objects.create(
                question='Question {}'.format(i),
                answer='Answer {}'.format(i),
                hint='Hint {}'.format(i),
                category=test_category,
            )
            self.test_cards.append(test_card)

    def test_braindump_index(self):
        """Test if the braindump index is displayed sucessfully
        """
        url = reverse('braindump-index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_braindump_session(self):
        """Test if the braindump session starts sucessfully
        """
        test_card = self.test_cards[0]

        url = reverse('braindump-session', args=(test_card.category.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

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
        test_category = Category.objects.create(name='Category 1337', description='Description 1337', mode=1)
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
        test_category = Category.objects.create(name='Category 1337', description='Description 1337', mode=2)
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
        test_category = Category.objects.create(name='Category 1337', description='Description 1337', mode=1)
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
        test_category = Category.objects.create(name='Category 1337', description='Description 1337', mode=2)
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

        self.assertEqual(Braindump.braindump_validate_min_max_area(DummyRequest), (1, 6))

    def test_validate_min_max_area_custom(self):
        """Test if custom min_area and max_area query string attributes can be validated properly
        """
        class DummyRequest:
            GET = {
                'min_area': 3,
                'max_area': 5,
            }

        self.assertEqual(Braindump.braindump_validate_min_max_area(DummyRequest), (3, 5))

    def test_generate_min_max_area_query_string_default(self):
        """Test if the query string for default min_area and max_area query string attributes can be generated properly
        """
        self.assertEqual(Braindump.braindump_generate_min_max_area_query_string(1, 6), '')

    def test_generate_min_max_area_query_string_custom(self):
        """Test if the query string for custom min_area and max_area query string attributes can be generated properly
        """
        self.assertEqual(Braindump.braindump_generate_min_max_area_query_string(2, 4), 'min_area=2&max_area=4')
        self.assertEqual(Braindump.braindump_generate_min_max_area_query_string(2, 6), 'min_area=2')
        self.assertEqual(Braindump.braindump_generate_min_max_area_query_string(1, 4), 'max_area=4')

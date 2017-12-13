from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ProtectedError
from django.test import TestCase, Client
from django.urls import reverse

from cards.models import Card
from categories.models import Category


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

    def test_category_list(self):
        """Test if the category list is displayed sucessfully
        """
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_category_detail(self):
        """Test if the category list is displayed sucessfully
        """
        test_card = self.test_cards[0]

        url = reverse('category-detail', args=(test_card.category.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

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

    def test_delete_non_empty_category(self):
        """Test if the "Delete" button does not work for category with cards
        """
        test_card = self.test_cards[3]

        with self.assertRaises(ProtectedError):
            url = reverse('category-delete', args=(test_card.category.pk,))
            response = self.client.post(url)
            self.assertEqual(response.status_code, 302)

        self.assertTrue(Category.objects.get(pk=test_card.category.pk))

    def test_delete_empty_category(self):
        """Test if the "Delete" button works for an empty category
        """
        test_category = Category.objects.create(name='Category 2', description='Description 2')

        url = reverse('category-delete', args=(test_category.pk,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        with self.assertRaises(ObjectDoesNotExist):
            Category.objects.get(pk=test_category.pk)

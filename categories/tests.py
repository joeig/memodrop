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

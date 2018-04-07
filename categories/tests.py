from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, Client
from django.urls import reverse

from cards.models import Card
from categories.models import Category


class CardTestCase(TestCase):
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

    def test_list(self):
        """Test if the category list is displayed sucessfully
        """
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        """Test if the category list is displayed sucessfully
        """
        test_card = self.test_cards[0]
        url = reverse('category-detail', args=(test_card.category.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_foreign_category_detail(self):
        """Test if the user has no access to foreign categories
        """
        test_user = User.objects.create_user('foreigner')
        test_category = Category.objects.create(
            name='Category 1337',
            description='Description 1337',
            owner=test_user
        )
        url = reverse('category-detail', args=(test_category.pk,))

        foreign_client = Client()
        foreign_client.force_login(test_user)
        foreign_response = foreign_client.get(url)
        self.assertEqual(foreign_response.status_code, 200)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_empty_category(self):
        """Test if the "Delete" button works for an empty category
        """
        test_category = Category.objects.create(name='Category 2', description='Description 2', owner=self.test_user)
        url = reverse('category-delete', args=(test_category.pk,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        with self.assertRaises(ObjectDoesNotExist):
            Category.objects.get(pk=test_category.pk)

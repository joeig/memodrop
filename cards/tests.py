from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, Client
from django.urls import reverse

from cards.models import Card
from categories.models import Category, ShareContract


class CardTestCase(TestCase):
    def setUp(self):
        """Set up test scenario
        """
        self.test_user = User.objects.create_user('test')
        self.test_category = Category.objects.create(name='Category 1', description='Description 1',
                                                     owner=self.test_user)
        self.client = Client()
        self.client.force_login(self.test_user)

        self.foreign_test_user = User.objects.create_user('card foreigner')

    def _create_test_card(self, suffix='', category=False):
        """Create a single test card
        """
        if not category:
            category = self.test_category
        card = Card.objects.create(
            question='Question'.format(suffix),
            answer='Answer'.format(suffix),
            hint='Hint'.format(suffix),
            category=category,
        )
        return card

    def test_list(self):
        """Test if the card list is displayed successfully
        """
        url = reverse('card-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        """Test if the card list is displayed sucessfully
        """
        test_card = self._create_test_card()
        url = reverse('card-detail', args=(test_card.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_foreign_card_detail(self):
        """Test if the user has no access to foreign cards
        """
        test_user = User.objects.create_user('foreigner')
        test_category = Category.objects.create(
            name='Category 1337',
            description='Description 1337',
            owner=test_user
        )
        test_card = self._create_test_card(category=test_category)
        url = reverse('card-detail', args=(test_card.pk,))

        foreign_client = Client()
        foreign_client.force_login(test_user)
        foreign_response = foreign_client.get(url)
        self.assertEqual(foreign_response.status_code, 200)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_delete(self):
        """Test if the "Delete" button works
        """
        test_card = self._create_test_card()
        url = reverse('card-delete', args=(test_card.pk,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        with self.assertRaises(ObjectDoesNotExist):
            Card.objects.get(pk=test_card.pk)

    def test_not_shared_card(self):
        """Test if a not shared card is actually not shared
        """
        test_category = Category.objects.create(name='Category', description='Description', owner=self.test_user)
        test_card = self._create_test_card(category=test_category)
        share_contract = ShareContract.objects.create(user=self.foreign_test_user, category=test_category)
        share_contract.decline()
        is_shared_with = Card.objects.get(pk=test_card.pk).is_shared_with()
        self.assertEqual(list(), is_shared_with)
        shared_objects = Card.shared_objects.all(user=self.foreign_test_user)
        self.assertEqual(list(), list(shared_objects))
        owned_objects = Card.owned_objects.all(user=self.test_user)
        self.assertEqual([test_card], list(owned_objects))

    def test_shared_card(self):
        """Test if a shared card is actually shared
        """
        test_category = Category.objects.create(name='Category', description='Description', owner=self.test_user)
        test_card = self._create_test_card(category=test_category)
        share_contract = ShareContract.objects.create(user=self.foreign_test_user, category=test_category)
        share_contract.accept()
        is_shared_with = Card.objects.get(pk=test_card.pk).is_shared_with()
        self.assertEqual([self.foreign_test_user], is_shared_with)
        shared_objects = Card.shared_objects.all(user=self.foreign_test_user)
        self.assertEqual([test_card], list(shared_objects))

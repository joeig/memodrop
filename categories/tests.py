from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, Client
from django.urls import reverse

from braindump.models import CardPlacement
from cards.models import Card
from categories.models import Category, ShareContract


class CategoryTestCase(TestCase):
    def setUp(self):
        """Set up test scenario
        """
        self.test_user = User.objects.create_user('test')
        self.test_category = Category.objects.create(name='Category 1', description='Description 1',
                                                     owner=self.test_user)
        self.client = Client()
        self.client.force_login(self.test_user)

        self.foreign_test_user = User.objects.create_user('category foreigner')
        self.foreign_test_category = Category.objects.create(name='Category Foreign', description='Description Foreign',
                                                             owner=self.foreign_test_user)
        self.foreign_client = Client()
        self.foreign_client.force_login(self.foreign_test_user)

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
        """Test if the category list is displayed successfully
        """
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        """Test if the category list is displayed successfully
        """
        test_card = self._create_test_card()
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

    def test_share_contract_list(self):
        """Test if the share contract list is displayed successfully
        """
        url = reverse('category-share-contract-list', args=(self.test_category.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_share_contract_request_valid_user(self):
        """Test if a share contract for a valid user works
        """
        url = reverse('category-share-contract-request', args=(self.test_category.pk,))
        response = self.client.post(url, data={'username': self.foreign_test_user.username})
        self.assertEqual(response.status_code, 302)
        share_contract = ShareContract.user_category_objects.all(user=self.foreign_test_user,
                                                                 category=self.test_category)
        self.assertTrue(share_contract.exists())

    def test_share_contract_request_owner(self):
        """Test if a share contract fails if the target user is equal to the owner of the category
        """
        url = reverse('category-share-contract-request', args=(self.test_category.pk,))
        response = self.client.post(url, data={'username': self.test_user.username})
        self.assertEqual(response.status_code, 200)
        share_contract = ShareContract.user_category_objects.all(user=self.test_user,
                                                                 category=self.test_category)
        self.assertFalse(share_contract.exists())

    def test_share_contract_request_invalid_user(self):
        """Test if a share contract for a invalid user doesn't work (but should respond exactly like a valid user)
        """
        url = reverse('category-share-contract-request', args=(self.test_category.pk,))
        response = self.client.post(url, data={'username': 'cake'})
        self.assertEqual(response.status_code, 302)
        share_contract = ShareContract.user_category_objects.all(user=self.foreign_test_user,
                                                                 category=self.test_category)
        self.assertFalse(share_contract.exists())

    def test_share_contract_request_foreign_category(self):
        """Test if a share contract for a invalid category doesn't work
        """
        url = reverse('category-share-contract-request', args=(self.foreign_test_category.pk,))
        response = self.client.post(url, data={'username': self.test_user.username})
        self.assertEqual(response.status_code, 404)
        share_contract = ShareContract.user_category_objects.all(user=self.foreign_test_user,
                                                                 category=self.foreign_test_category)
        self.assertFalse(share_contract.exists())

    def test_share_contract_accept(self):
        """Test if a share contract can be accepted
        """
        test_category = Category.objects.create(name='Category', description='Description', owner=self.test_user)
        test_card = self._create_test_card(category=test_category)
        share_contract = ShareContract.objects.create(user=self.foreign_test_user, category=test_category)
        url = reverse('category-share-contract-accept', args=(share_contract.pk,))
        response = self.foreign_client.post(url, data={'decision': 'Accept'})
        self.assertEqual(response.status_code, 302)
        refreshed_share_contract = ShareContract.objects.get(pk=share_contract.pk)
        self.assertTrue(refreshed_share_contract.accepted)
        test_card_placement = CardPlacement.objects.filter(card=test_card, user=self.foreign_test_user)
        self.assertTrue(test_card_placement.exists())

    def test_share_contract_decline(self):
        """Test if a share contract can be declined
        """
        share_contract = ShareContract.objects.create(user=self.foreign_test_user, category=self.test_category)
        url = reverse('category-share-contract-accept', args=(share_contract.pk,))
        response = self.foreign_client.post(url, data={'decision': 'Decline'})
        self.assertEqual(response.status_code, 302)
        refreshed_share_contract = ShareContract.objects.filter(pk=share_contract.pk).all()
        self.assertFalse(refreshed_share_contract.exists())

    def test_share_contract_revoke(self):
        """Test if a share contract can be revoked
        """
        rand = User.objects.make_random_password(length=32)
        test_category = Category.objects.create(name=rand, description='Description', owner=self.test_user)
        test_card = self._create_test_card(category=test_category)
        share_contract = ShareContract.objects.create(user=self.foreign_test_user, category=test_category)
        share_contract.accept()
        card_placement = CardPlacement.objects.get(user=self.foreign_test_user, card=test_card)
        url = reverse('category-share-contract-revoke', args=(test_category.pk, share_contract.pk,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        refreshed_share_contract = ShareContract.objects.filter(pk=share_contract.pk).all()
        self.assertFalse(refreshed_share_contract.exists())
        refreshed_card_placement = CardPlacement.objects.filter(
            user=self.foreign_test_user,
            card__category__name=rand,
        ).first()
        self.assertNotEqual(card_placement.card, refreshed_card_placement.card)

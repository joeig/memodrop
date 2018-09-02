from django.conf import settings
from django.db import models
from django.urls import reverse

from categories.exceptions import ShareContractAlreadyRevoked, ShareContractCannotBeAccepted, \
    ShareContractCannotBeDeclined, ShareContractCannotBeRevoked
from categories.signals import share_contract_accepted, share_contract_revoked


class CategoryOwnerManager(models.Manager):
    def all(self, owner):
        """Returns all categories belonging to the owner
        """
        return self.filter(owner=owner).all()

    def get(self, owner, *args, **kwargs):
        """Returns a category belonging to the owner
        """
        return self.filter(owner=owner).get(*args, **kwargs)


class CategorySharedManager(models.Manager):
    def all(self, user):
        """Returns all categories shared with the user
        """
        return self.filter(share_contracts__user=user, share_contracts__accepted=True).all()

    def get(self, user, *args, **kwargs):
        """Returns a category shared with the user
        """
        return self.filter(share_contracts__user=user, share_contracts__accepted=True).get(*args, **kwargs)


class Category(models.Model):
    MODE_CHOICES = (
        (1, 'Strict'),
        (2, 'Defensive'),
    )
    name = models.CharField(max_length=128)
    description = models.TextField(verbose_name='Description')
    mode = models.IntegerField(default=1, choices=MODE_CHOICES)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    objects = models.Manager()
    owned_objects = CategoryOwnerManager()
    shared_objects = CategorySharedManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Get the absolute URL to a single card
        """
        return reverse('category-detail', kwargs={'pk': self.pk})

    def get_cards_for_area(self, area):
        """Get all cards of a specific area
        """
        return self.cards.filter(area=area)

    def is_shared_with(self):
        """Returns a list of users this category is shared with
        """
        return [s.user for s in self.share_contracts.filter(accepted=True)]


class ShareContractUserManager(models.Manager):
    def all(self, user):
        """Returns all share contracts belonging to the authorized user
        """
        return self.filter(user=user).all()

    def get(self, user, *args, **kwargs):
        """Returns a share contract belonging to the authorized user
        """
        return self.filter(user=user).get(*args, **kwargs)


class ShareContractCategoryManager(models.Manager):
    def all(self, category):
        """Returns all share contracts belonging to a category
        """
        return self.filter(category=category).all()

    def get(self, category, *args, **kwargs):
        """Returns a share contract belonging to a category
        """
        return self.filter(category=category).get(*args, **kwargs)


class ShareContractUserCategoryManager(models.Manager):
    def all(self, user, category):
        """Returns all share contracts belonging to the authorized user
        """
        return self.filter(user=user, category=category).all()

    def get(self, user, category, *args, **kwargs):
        """Returns a share contract belonging to the authorized user
        """
        return self.filter(user=user, category=category).get(*args, **kwargs)


class ShareContract(models.Model):
    """ShareContract

    Workflow:
    -> Create
        self.accepted = False
        self.revoked = False
        -> Accept
            self.accepted = True
            self.revoked = False
            -> Revoke
                self.accepted = True
                self.revoked = True
                -> Delete
        -> Decline
            -> Delete
    """
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE, related_name='share_contracts')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    revoked = models.BooleanField(default=False)
    objects = models.Manager()
    user_objects = ShareContractUserManager()
    category_objects = ShareContractCategoryManager()
    user_category_objects = ShareContractUserCategoryManager()

    class Meta:
        unique_together = (('category', 'user'),)

    def accept(self):
        """Accept this share contract
        """
        if self.accepted or self.revoked:
            raise ShareContractCannotBeAccepted()
        self.accepted = True
        self.save()
        share_contract_accepted.send(sender=self.__class__, share_contract=self)

    def decline(self):
        """Decline this share contract
        """
        if self.accepted or self.revoked:
            raise ShareContractCannotBeDeclined()
        self.delete()

    def revoke(self):
        """Revoke this share contract
        """
        if not self.accepted:
            raise ShareContractCannotBeRevoked()
        if self.revoked:
            raise ShareContractAlreadyRevoked()
        self.revoked = True
        self.save()
        share_contract_revoked.send(sender=self.__class__, share_contract=self)

from django import forms
from django.contrib.auth.models import User
from django.db import IntegrityError

from categories.exceptions import ShareContractUserIsOwner, ShareContractAlreadyExists, ShareContractUserDoesNotExist
from categories.models import ShareContract


class ShareContractForm(forms.Form):
    username = forms.CharField(label='Username')

    def create_share_contract(self, category, requester_user):
        """Creates a new share contract if the user exists
        """
        user_query_set = User.objects.filter(username=self.cleaned_data['username'])
        if user_query_set.exists():
            if user_query_set.first() == requester_user:
                # Raise exception in case that the target user is the owner of the category (circular dependency):
                raise ShareContractUserIsOwner()
            try:
                return ShareContract.objects.create(
                    category=category,
                    user=user_query_set.first(),
                )
            except IntegrityError:
                # Raise exception in case that this ShareContract already exists (unique key constraint):
                raise ShareContractAlreadyExists()
        else:
            # Raise exception in case that the requested User does not exist:
            raise ShareContractUserDoesNotExist()

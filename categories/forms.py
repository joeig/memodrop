from django import forms
from django.contrib.auth.models import User
from django.db import IntegrityError

from categories.models import ShareContract


class ShareContractForm(forms.Form):
    username = forms.CharField(label='Username')

    def create_share_contract(self, category):
        """Creates a new share contract if the user exists

        Return False if something goes wrong, because we don't want to expose existing usernames.
        """
        user_query_set = User.objects.filter(username=self.cleaned_data['username'])
        if user_query_set.exists():
            try:
                return ShareContract.objects.create(
                    category=category,
                    user=user_query_set.first(),
                )
            except IntegrityError:
                # Return False in case that this ShareContract already exists (unique key constraint):
                return False
        else:
            # Return False in case that the requested User does not exist:
            return False

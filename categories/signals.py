from django.dispatch import Signal

share_contract_accepted = Signal(providing_args=['pk'])
share_contract_revoked = Signal(providing_args=['pk'])

from django.contrib import messages
from django.urls import reverse
from django.views.generic import RedirectView


class PasswordChangeDoneView(RedirectView):
    """Renders the password change done view
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        messages.info(self.request, 'Your password was changed.')
        return reverse('index')

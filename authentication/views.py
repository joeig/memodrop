from categories.models import Category
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import RedirectView, TemplateView


class PasswordChangeDoneView(RedirectView):
    """Renders the password change done view
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        messages.info(self.request, 'Your password was changed.')
        return reverse('index')


class ProfileView(LoginRequiredMixin, TemplateView):
    """Renders the user's profile
    """
    template_name = 'auth/profile.html'

    def get_context_data(self, **kwargs):
        owned_category_count = Category.owned_objects.all(self.request.user).count()
        shared_category_count = Category.shared_objects.all(self.request.user).count()
        total_category_count = owned_category_count + shared_category_count

        owned_card_count = 0
        for category in Category.owned_objects.all(self.request.user):
            owned_card_count += category.cards.count()

        shared_card_count = 0
        for category in Category.shared_objects.all(self.request.user):
            shared_card_count += category.cards.count()

        total_card_count = owned_card_count + shared_card_count

        context = {
            'owned_category_count': owned_category_count,
            'shared_category_count': shared_category_count,
            'total_category_count': total_category_count,
            'owned_card_count': owned_card_count,
            'shared_card_count': shared_card_count,
            'total_card_count': total_card_count,
        }

        return context

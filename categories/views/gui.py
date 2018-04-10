from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from braindump.models import CardPlacement
from categories.models import Category


class CategoryBelongsOwnerMixin:
    """Mixin that returns all categories owned by the authorized user
    """
    def get_queryset(self):
        return Category.owned_objects.all(self.request.user)


class CategoryBelongsUserMixin:
    """Mixin that returns all categories belonging to the authorized user
    """
    def get_queryset(self):
        owned_category_list = Category.owned_objects.all(self.request.user)
        shared_category_list = Category.shared_objects.all(self.request.user)
        return owned_category_list | shared_category_list


class CategoryList(LoginRequiredMixin, CategoryBelongsUserMixin, ListView):
    """List all categories
    """
    paginate_by = 25
    paginate_orphans = 5


class CategoryDetail(LoginRequiredMixin, CategoryBelongsUserMixin, DetailView):
    """Show detailed information about a category
    """
    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        context['card_placements'] = CardPlacement.user_objects.all(self.request.user).filter(
            card__category=self.object.id,
        ).all()

        for i in range(1, 7):
            context['area{}'.format(i)] = CardPlacement.user_objects.all(self.request.user).filter(
                card__category=self.object.id,
                area=i,
            ).all()

        return context


class CategoryCreate(LoginRequiredMixin, CategoryBelongsUserMixin, CreateView):
    """Create a new category
    """
    model = Category
    fields = ['name', 'description', 'mode']
    template_name_suffix = '_create_form'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['description'].help_text = 'You can use Markdown.'
        form.fields['mode'].help_text = """
<strong>Strict Mode:</strong> Incorrectly answered cards are moved back to the first area.<br>
<strong>Defensive Mode:</strong> Incorrectly answered cards are moved back to the previous area.
"""
        return form

    def form_valid(self, form):
        messages.success(self.request, 'Category created.')
        form.instance.owner = self.request.user
        return super(CategoryCreate, self).form_valid(form)


class CategoryUpdate(LoginRequiredMixin, CategoryBelongsOwnerMixin, UpdateView):
    """Update a category
    """
    fields = ['name', 'description', 'mode']
    template_name_suffix = '_update_form'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['description'].help_text = 'You can use Markdown.'
        form.fields['mode'].help_text = """
<strong>Strict Mode:</strong> Incorrectly answered cards are moved back to the first area.<br>
<strong>Defensive Mode:</strong> Incorrectly answered cards are moved back to the previous area.
"""
        return form

    def form_valid(self, form):
        messages.success(self.request, 'Category updated.')
        return super(CategoryUpdate, self).form_valid(form)


class CategoryDelete(LoginRequiredMixin, CategoryBelongsOwnerMixin, DeleteView):
    """Delete a category
    """
    success_url = reverse_lazy('category-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Category deleted.')
        return super(CategoryDelete, self).delete(request, *args, **kwargs)

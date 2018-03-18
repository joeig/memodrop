from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from cards.models import Card
from categories.models import Category


class CategoryBelongsUserMixin:
    """Mixin that returns all categories belonging to the authorized user
    """
    def get_queryset(self):
        return Category.objects.all_of_user(self.request.user)


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
        context['area1'] = Card.objects.filter(category_id=self.object.id, area=1).all()
        context['area2'] = Card.objects.filter(category_id=self.object.id, area=2).all()
        context['area3'] = Card.objects.filter(category_id=self.object.id, area=3).all()
        context['area4'] = Card.objects.filter(category_id=self.object.id, area=4).all()
        context['area5'] = Card.objects.filter(category_id=self.object.id, area=5).all()
        context['area6'] = Card.objects.filter(category_id=self.object.id, area=6).all()
        return context


class CategoryCreate(LoginRequiredMixin, CategoryBelongsUserMixin, CreateView):
    """Create a new category
    """
    model = Category
    fields = ['name', 'description', 'mode']
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        messages.success(self.request, 'Category created.')
        form.instance.owner = self.request.user
        return super(CategoryCreate, self).form_valid(form)


class CategoryUpdate(LoginRequiredMixin, CategoryBelongsUserMixin, UpdateView):
    """Update a category
    """
    fields = ['name', 'description', 'mode']
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        messages.success(self.request, 'Category updated.')
        return super(CategoryUpdate, self).form_valid(form)


class CategoryDelete(LoginRequiredMixin, CategoryBelongsUserMixin, DeleteView):
    """Delete a category
    """
    success_url = reverse_lazy('category-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Category deleted.')
        return super(CategoryDelete, self).delete(request, *args, **kwargs)

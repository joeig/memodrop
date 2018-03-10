from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from cards.models import Card
from categories.models import Category


class CategoryList(ListView):
    """List all categories
    """
    model = Category
    paginate_by = 25
    paginate_orphans = 5


class CategoryDetail(DetailView):
    """Show detailed information about a category
    """
    model = Category

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        context['area1'] = Card.objects.filter(category_id=self.object.id, area=1).all()
        context['area2'] = Card.objects.filter(category_id=self.object.id, area=2).all()
        context['area3'] = Card.objects.filter(category_id=self.object.id, area=3).all()
        context['area4'] = Card.objects.filter(category_id=self.object.id, area=4).all()
        context['area5'] = Card.objects.filter(category_id=self.object.id, area=5).all()
        context['area6'] = Card.objects.filter(category_id=self.object.id, area=6).all()
        return context


class CategoryCreate(CreateView):
    """Create a new category
    """
    model = Category
    fields = ['name', 'description', 'mode']
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        messages.success(self.request, 'Category created.')
        return super(CategoryCreate, self).form_valid(form)


class CategoryUpdate(UpdateView):
    """Update a category
    """
    model = Category
    fields = ['name', 'description', 'mode']
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        messages.success(self.request, 'Category updated.')
        return super(CategoryUpdate, self).form_valid(form)


class CategoryDelete(DeleteView):
    model = Category
    success_url = reverse_lazy('category-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Category deleted.')
        return super(CategoryDelete, self).delete(request, *args, **kwargs)

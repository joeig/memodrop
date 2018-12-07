from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import ListView, View, DeleteView, FormView

from categories.exceptions import ShareContractAlreadyRevoked, ShareContractUserIsOwner, \
    ShareContractUserDoesNotExist, ShareContractAlreadyExists
from categories.forms import ShareContractForm
from categories.models import Category, ShareContract


class ShareContractBelongsOwnerMixin:
    """Mixin that returns all share contracts belonging to the authorized user
    """
    def get_queryset(self):
        category = get_object_or_404(Category.owned_objects.all(self.request.user), pk=self.kwargs['pk'])
        return ShareContract.category_objects.all(category=category).filter(accepted=True)


class ShareContractBelongsUserMixin:
    """Mixin that returns all share contracts belonging to the authorized user
    """
    def get_queryset(self):
        return ShareContract.user_objects.all(self.request.user)


class CategoryShareContractList(LoginRequiredMixin, ShareContractBelongsOwnerMixin, ListView):
    """List all share contracts
    """
    paginate_by = 25
    paginate_orphans = 5

    def get_context_data(self, **kwargs):
        category = get_object_or_404(Category.owned_objects.all(self.request.user), pk=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context


class CategoryShareContractRequest(LoginRequiredMixin, FormView):
    """Request a share contract
    """
    template_name = 'categories/sharecontract_request_form.html'
    form_class = ShareContractForm

    def form_valid(self, form):
        category = get_object_or_404(Category.owned_objects.all(self.request.user), pk=self.kwargs['pk'])
        try:
            form.create_share_contract(category=category, requester_user=self.request.user)
        except ShareContractUserIsOwner:
            messages.error(self.request, 'You cannot share your category with yourself.')
            return self.render_to_response(self.get_context_data(form=form))
        except (ShareContractAlreadyExists, ShareContractUserDoesNotExist):
            # Pass these errors for privacy reasons (we do not want to expose user names):
            pass
        messages.info(self.request, 'The invitation has been sent successfully (assuming that the user exists).')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('category-detail', args=(self.kwargs['pk'],))


class CategoryShareContractRevoke(LoginRequiredMixin, ShareContractBelongsOwnerMixin, DeleteView):
    """Delete a share contract
    """
    pk_url_kwarg = 'share_contract_pk'
    context_object_name = 'share_contract'

    def delete(self, request, *args, **kwargs):
        share_contract = self.get_object()
        success_url = self.get_success_url()
        try:
            share_contract.revoke()
        except ShareContractAlreadyRevoked:
            messages.error(
                self.request,
                mark_safe('Access revocation for {} is already in progress.'.format(share_contract.user))
            )
        else:
            messages.success(
                self.request,
                mark_safe('Access for {} will be revoked.'.format(share_contract.user))
            )
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse('category-share-contract-list', args=(self.kwargs['pk'],))


class CategoryShareContractAccept(LoginRequiredMixin, ShareContractBelongsUserMixin, View):
    """Accept a share contract
    """
    http_method_names = ['get', 'post']

    def get(self, request, share_contract_pk):
        share_contract = get_object_or_404(self.get_queryset(), pk=share_contract_pk, accepted=False)
        context = {
            'share_contract': share_contract,
        }
        return render(request, 'categories/sharecontract_confirm_accept.html', context)

    def post(self, request, share_contract_pk):
        share_contract = get_object_or_404(self.get_queryset(), pk=share_contract_pk)
        if request.POST.get('decision') == 'Accept':
            share_contract.accept()
            messages.success(request, 'Access granted.')
            return redirect(reverse('category-detail', args=(share_contract.category.pk,)))
        else:
            share_contract.decline()
            messages.info(request, 'Invitation declined.')
            return redirect(reverse('index'))

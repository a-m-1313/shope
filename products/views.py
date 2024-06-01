from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.utils.translation import gettext as _

from products.forms import CommentForm
from products.models import Product, Comment
from cart.forms import AddToCartProductForm


class ProductListView(generic.ListView):
    queryset = Product.objects.filter(active=True)
    template_name = 'pages/product_list.html'
    context_object_name = 'products'


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'pages/detail_view.html'
    context_object_name = 'detail_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = CommentForm()
        context['add_to_cart_form'] = AddToCartProductForm()
        return context


class CommentCreateView(generic.CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user

        product_id = int(self.kwargs['product_id'])
        product = get_object_or_404(Product, id=product_id)
        obj.product = product

        messages.success(message=_('submit comment'), request=self.request)

        return super().form_valid(form)










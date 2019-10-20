from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import JsonResponse
from basketapp.models import Basket
from mainapp.models import Product
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy


class BasketListView(ListView):
    model = Basket
    template_name = 'basketapp/basket.html'

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(BasketListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user).order_by('product__category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'корзина'

        return context


@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))
        
    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class BasketDeleteView(DeleteView):
    model = Basket
    success_url = reverse_lazy('basket:view')

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(BasketDeleteView, self).dispatch(request, *args, **kwargs)


class BasketUpdateView(UpdateView):
    model = Basket
    template_name = 'basketapp/includes/inc_basket_list.html'
    fields = '__all__'

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(BasketUpdateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        quantity = int(self.kwargs['quantity'])

        if quantity > 0:
            self.object.quantity = quantity
            self.object.save()
        else:
            self.object.delete()

        qs = list(self.get_queryset())

        content = {
            'object_list': qs
        }

        result = render_to_string('basketapp/includes/inc_basket_list.html',\
                                  content)

        return JsonResponse({'result': result})

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user).order_by('product__category')


# @login_required
# def basket_edit(request, pk, quantity):
#     if request.is_ajax():
#         quantity = int(quantity)
#         new_basket_item = Basket.objects.get(pk=int(pk))
#
#         if quantity > 0:
#             new_basket_item.quantity = quantity
#             new_basket_item.save()
#         else:
#             new_basket_item.delete()
#
#         basket_items = Basket.objects.filter(user=request.user).\
#                                             order_by('product__category')
#
#         content = {
#             'object_list': basket_items,
#         }
#
#         result = render_to_string('basketapp/includes/inc_basket_list.html',\
#                                   content)
#
#         return JsonResponse({'result': result})
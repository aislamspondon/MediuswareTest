from django.shortcuts import HttpResponseRedirect, render
from django.views import generic
from django.views.generic import CreateView, ListView, UpdateView

from product.forms import VariantForm
from product.models import Variant


class BaseVariantView(generic.View):
    form_class = VariantForm
    model = Variant
    template_name = 'variants/create.html'
    success_url = '/product/variants'


class VariantView(BaseVariantView, ListView):
    template_name = 'variants/list.html'
    paginate_by = 10

    def get_queryset(self):
        filter_string = {}
        print(self.request.GET)
        for key in self.request.GET:
            if self.request.GET.get(key):
                filter_string[key] = self.request.GET.get(key)
        return Variant.objects.filter(**filter_string)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = True
        context['request'] = ''
        if self.request.GET:
            context['request'] = self.request.GET['title__icontains']
        return context

    


class VariantCreateView(BaseVariantView, CreateView):
    def post(self, request):
        variant_form = VariantForm(request.POST)
        data = request.POST
        if variant_form.is_valid:
            if data['active'] == 'on':
                variant_title = data['title']
                variant_desc = data['description']
                variant_active = True
                Variant.objects.create(
                    title=variant_title,
                    description = variant_desc,
                    active = variant_active
                )
        return HttpResponseRedirect('/product/variants/')


class VariantEditView(BaseVariantView, UpdateView):
    pk_url_kwarg = "id"
    def post(self, request):
        
        return HttpResponseRedirect('/') 

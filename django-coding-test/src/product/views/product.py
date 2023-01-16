import json

from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect, render
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from product.forms import ProductForm, VariantForm
from product.models import (Product, ProductVariant, ProductVariantPrice,
                            Variant)


@method_decorator(csrf_exempt, name='dispatch')
class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'
    
    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        product = Product.objects.all()
        context['product'] = product
        context['variants'] = list(variants.all())
        return context
    def post(self, request):
        # print("This is",request.body)
        json_data = json.loads(request.body)
        data = json_data['data']
        title =data['title'] 
        sku = data['slug']
        description = data['description']
        variantPrices = data['variantPrice']
        print(variantPrices, "MOma")
        variants = data['variants']
        product = Product.objects.create(
            title = title,
            sku = sku,
            description = description
        )
        for variant in range(0, len(variants)):
            variant_id = variants[variant]['option']
            tags= variants[variant]['tags']
            
            variant_name = Variant.objects.get(id=variant_id)
            for variantPrice in range(0,len(variantPrices)):
                variant_pro = variantPrices[variantPrice]
                variant_title = variant_pro['title']
                variant_split = variant_title.split('/')
                variant_tags = variant_split[0:-1]
                for tag in tags:
                    
                    if tag in variant_tags:
                        ProductVariant.objects.create(
                            variant_title = variant_title,
                            variant = variant_name,
                            product = Product.objects.get(id=product.id)
                            )
        for variantPrice in range(0, len(variantPrices)):
            variant_pro = variantPrices[variantPrice]
            variant_title = variant_pro['title']
            qs = ProductVariant.objects.filter(variant_title = variant_title).first()
            print(variant_pro['price'])
            print(variant_pro['stock'])
            ProductVariantPrice.objects.create(
                product_variant_one = qs,
                price = variant_pro['price'],
                stock = variant_pro['stock'],
                product = Product.objects.get(id=product.id)
            )
        return HttpResponseRedirect('/')

class ProductListView(generic.TemplateView):
    template_name = 'products/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # fm = StudentRegistration()
        products = Product.objects.all()
        paginator = Paginator(products, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        variants = ProductVariantPrice.objects.all()
        total_product = products.count()
        highnumber = int(page_number)*10
        # for product in products:
        #     for variant in variants:
        #         if variant.product == product:
        #             print("This")
        
        context = { 'variants': variants, 'page_obj': page_obj, "total": total_product, 'highest': highnumber}
        return context



from django.contrib import admin

from product.models import (Product, ProductImage, ProductVariant,
                            ProductVariantPrice, Variant)

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(ProductImage)
admin.site.register(Variant)
admin.site.register(ProductVariantPrice)

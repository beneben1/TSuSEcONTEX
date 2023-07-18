from django.contrib import admin

# Register your models here.
from .models import Orders, Product


admin.site.register(Product)
admin.site.register(Orders)


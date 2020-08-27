from django.contrib import admin

# Register your models here.
from .models import Stock, DetailPage, Price

admin.site.register(Stock)

admin.site.register(DetailPage)

admin.site.register(Price)


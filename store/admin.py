from django.contrib import admin
from .models import storeItem, storeCategory, cartEntry

admin.site.register(storeItem)
admin.site.register(storeCategory)
admin.site.register(cartEntry)

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class storeCategory(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=100)
    parent_id = models.ForeignKey("storeCategory", on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.name

def get_media_path(instance, filename):
    return 'items/{0}/{1}'.format(instance.name, filename)

class storeItem(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to=get_media_path)
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category_id = models.ForeignKey(storeCategory, on_delete=models.SET_NULL, null=True, blank=True)
    inStock = models.IntegerField()
    def __str__(self):
        return self.name

class cartEntry(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    item_id = models.ForeignKey(storeItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return self.item_id.name
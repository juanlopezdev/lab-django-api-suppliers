from django.db import models
from django.contrib.auth.models import User
from .constants import PURCHASE_STATE_CHOICES, STATE_CHOICES, ACTIVE, PENDING

class Supplier(models.Model):
    name = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    is_partnership = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.SmallIntegerField(default=ACTIVE, choices=STATE_CHOICES)

    def __str__(self):
        return self.name

class Product(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=False)
    description = models.CharField(max_length=255)
    url = models.URLField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.SmallIntegerField(default=ACTIVE, choices=STATE_CHOICES)

    def __str__(self):
        return self.description

class PurchaseRequest(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_state = models.IntegerField(choices=PURCHASE_STATE_CHOICES, default=PENDING)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_purchase_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.SmallIntegerField(default=ACTIVE, choices=STATE_CHOICES)

    def __str__(self):
        return str(self.id)

class PurchaseRequestDetail(models.Model):
    purchase_request = models.ForeignKey(PurchaseRequest, related_name='details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_unit = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.SmallIntegerField(default=ACTIVE, choices=STATE_CHOICES)


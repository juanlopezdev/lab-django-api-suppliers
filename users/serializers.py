from django.contrib.auth.models import Group, User
from .models import Supplier, Product, PurchaseRequest, PurchaseRequestDetail
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ['state']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['state']

class PurchaseRequestSerializer(serializers.ModelSerializer):
    approved_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(groups__name='Aprobador'),
        allow_null= True,
        required=False
    )

    class Meta:
        model = PurchaseRequest
        fields = '__all__'
        read_only_fields = ['state']

class PurchaseRequestDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseRequestDetail
        fields = '__all__'
        read_only_fields = ['state']
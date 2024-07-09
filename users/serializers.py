from django.contrib.auth.models import Group, User
from .models import Supplier, Product, PurchaseRequest, PurchaseRequestDetail
from rest_framework import serializers
from .constants import ACTIVE

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'groups']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ['state']

class ProductSerializer(serializers.ModelSerializer):
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['state']
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['supplier'] = SupplierSerializer(instance.supplier).data
        return response

class PurchaseRequestSerializer(serializers.ModelSerializer):
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())
    approved_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(groups__name='Aprobador'),
        allow_null= True,
        required=False
    )

    class Meta:
        model = PurchaseRequest
        fields = '__all__'
        read_only_fields = ['state']
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['supplier'] = SupplierSerializer(instance.supplier).data if instance.supplier else None
        response['approved_by'] = UserSerializer(instance.approved_by).data if instance.approved_by else None
        return response

class PurchaseRequestDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseRequestDetail
        fields = '__all__'
        read_only_fields = ['state']
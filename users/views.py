from django.shortcuts import render
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets

from tutorial.quickstart.serializers import GroupSerializer, UserSerializer
from .models import Supplier, Product, PurchaseRequest, PurchaseRequestDetail
from .serializers import SupplierSerializer, ProductSerializer, PurchaseRequestSerializer, PurchaseRequestDetailSerializer
from .permissions import CanApproveOrReject, CanInsertOrDeletePaymentRequest

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all().order_by('-created_at')
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

class PurchaseRequestViewSet(viewsets.ModelViewSet):
    queryset = PurchaseRequest.objects.all().order_by('-created_at')
    serializer_class = PurchaseRequestSerializer
    permission_classes = [
        permissions.IsAuthenticated, 
        permissions.DjangoModelPermissions, 
        CanApproveOrReject,
        CanInsertOrDeletePaymentRequest
    ]

class PurchaseRequestDetailViewSet(viewsets.ModelViewSet):
    queryset = PurchaseRequestDetail.objects.all()
    serializer_class = PurchaseRequestDetailSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
from django.shortcuts import render
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

# from tutorial.quickstart.serializers import GroupSerializer, UserSerializer
from .models import Supplier, Product, PurchaseRequest, PurchaseRequestDetail
from .serializers import UserSerializer, GroupSerializer, SupplierSerializer, ProductSerializer, PurchaseRequestSerializer, PurchaseRequestDetailSerializer
from .permissions import CanApproveOrRejectPaymentRequestPermission, CanInsertOrDeletePaymentRequest, CanUpdatePaymentRequestPermission
from .utils import transform_string_to_int as utils_transform_string_to_int
from .constants import ACTIVE, INACTIVE

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.filter(state=ACTIVE).order_by('-created_at')
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def destroy(self, request, *args, **pk):
        supplier = self.get_object()
        supplier.state = INACTIVE
        supplier.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(state=ACTIVE).order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def destroy(self, request, *args, **pk):
        product = self.get_object()
        product.state = INACTIVE
        product.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PurchaseRequestViewSet(viewsets.ModelViewSet):
    queryset = PurchaseRequest.objects.filter(state=ACTIVE).order_by('-created_at')
    serializer_class = PurchaseRequestSerializer
    permission_classes = [
        permissions.IsAuthenticated, 
        permissions.DjangoModelPermissions, 
        CanInsertOrDeletePaymentRequest,
        CanUpdatePaymentRequestPermission
    ]

    @action(detail=True, methods=['patch'], url_path='approve-request', permission_classes=[CanApproveOrRejectPaymentRequestPermission])
    def approve_request(self, request, pk=None):
        if 'approved_by' not in request.data or 'purchase_state' not in request.data:
            return Response({'error': 'Missing fields'}, status=status.HTTP_400_BAD_REQUEST)

        purchase_request = self.get_object()
        serializer = self.get_serializer(purchase_request, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        approved_by_id = request.data.get('approved_by')
        purchase_state = request.data.get('purchase_state')
        purchase_request.approved_by = User.objects.get(id=approved_by_id)
        purchase_request.purchase_state = purchase_state
        purchase_request.save()

        return Response({'status': 'Updated purchase request'})

    def destroy(self, request, *args, **pk):
        purchase_request = self.get_object()
        purchase_request.state = INACTIVE
        purchase_request.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PurchaseRequestDetailViewSet(viewsets.ModelViewSet):
    queryset = PurchaseRequestDetail.objects.filter(state=ACTIVE)
    serializer_class = PurchaseRequestDetailSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def destroy(self, request, *args, **pk):
        purchase_request_detail = self.get_object()
        purchase_request_detail.state = INACTIVE
        purchase_request_detail.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
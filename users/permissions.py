from rest_framework import permissions
from django.utils.translation import gettext_lazy as _

from .utils import transform_string_to_int as utils_transform_string_to_int, is_empty_value as utils_is_empty_value

class CanApproveOrRejectPaymentRequestPermission(permissions.BasePermission):
    message = _("Only users with 'Approver' permissions can perform this action.")

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if view.action == 'approve_request':
            return request.user.groups.filter(name='Aprobador').exists()

        return True          

    def has_object_permission(self, request, view, obj):
        method = request.method

        if method in permissions.SAFE_METHODS:
            return True

        if method == 'PATCH' and request.data:
            return self.handle_patch(request)

        return True
    
    def handle_patch(self, request):
        if 'purchase_state' in request.data or 'approved_by' in request.data:
            is_approver_user = request.user.groups.filter(name='Aprobador').exists()
            if not is_approver_user: 
                self.message = _("A 'Setter' user cannot update the status or approve a purchase request")
            return is_approver_user
        return True

class CanInsertOrDeletePaymentRequest(permissions.BasePermission):
    message = _('You do not have permission to perform this action')

    def has_permission(self, request, view):
        is_colocador_user = request.user.groups.filter(name='Colocador').exists()
        method = request.method

        if method in permissions.SAFE_METHODS:
            return True
        if method == 'DELETE':
            return self.handle_delete(is_colocador_user)
        if method == 'POST':
            return self.handle_post(request, is_colocador_user)
        return True

    def handle_delete(self, is_colocador_user):
        if not is_colocador_user:
            self.message = _("Only users in the 'Setter' group can delete.")
            return False
        return True
    
    def handle_post(self, request, is_colocador_user):
        if not is_colocador_user:
            self.message = _("Only users in the 'Setter' group can create purchase requests.")
            return False

        if request.method == 'POST' and request.data:
            purchase_state = request.data.get('purchase_state')
            purchase_state = utils_transform_string_to_int(purchase_state)
            approved_by = request.data.get('approved_by')

            if purchase_state != 0 or not utils_is_empty_value(approved_by):
                self.message = _("Invalid operation for users in the 'Setter' group.")
                return False
        return True

class CanUpdatePaymentRequestPermission():
    message = _('You do not have permission to perform this action')

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return True        

    def has_object_permission(self, request, view, obj):
        method = request.method

        if method in permissions.SAFE_METHODS:
            return True
        
        is_colocador_user = request.user.groups.filter(name='Colocador').exists()
        
        if method in ['PUT', 'PATCH']:
            return self.handle_put(request, is_colocador_user)

        return True

    def handle_put(self, request, is_colocador_user):
        if request.data and is_colocador_user:
            purchase_state = request.data.get('purchase_state')
            purchase_state = utils_transform_string_to_int(purchase_state)
            approved_by = request.data.get('approved_by')
            if purchase_state != 0 or not utils_is_empty_value(approved_by):
                self.message = _("A 'Setter' user cannot update the status or approve a purchase request")
                return False
        return True
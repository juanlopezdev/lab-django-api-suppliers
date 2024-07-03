from rest_framework import permissions
from django.utils.translation import gettext_lazy as _


class CanApproveOrReject(permissions.BasePermission):
    message = _("Only users with 'Approver' permissions can perform this action.")

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return True          

    def has_object_permission(self, request, view, obj):
        method = request.method

        if method in permissions.SAFE_METHODS:
            return True

        if method in ['PUT', 'PATCH'] and 'purchase_state' in request.data or 'approved_by' in request.data:
            return request.user.groups.filter(name='Aprobador').exists()

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
        if 'purchase_request' in request.data or 'approved_by' in request.data:
            self.message = _("Invalid operation for users in the 'Setter' group.")
            return False
        return True
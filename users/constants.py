
ACTIVE = 1
INACTIVE = 0

STATE_CHOICES = (
    (ACTIVE, 'Activo'),
    (INACTIVE, 'Inactivo'),
)

PENDING = 0
APPROVED = 1
REJECTED = 2

PURCHASE_STATE_CHOICES = (
    (PENDING, 'Pendiente'),
    (APPROVED, 'Aprobado'),
    (REJECTED, 'Rechazado'),
)
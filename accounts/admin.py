from django.contrib import admin

from .models import (
    Role,
    Permission,
    User,
    UserRole,
    RolePermission,
    AuditLog
)

admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(User)
admin.site.register(UserRole)
admin.site.register(RolePermission)
admin.site.register(AuditLog)
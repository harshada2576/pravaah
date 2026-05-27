from django.db import models
from django.contrib.auth.models import AbstractUser
class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(
        max_length=100,
        unique=True
    )
    description = models.TextField()
    is_active = models.BooleanField(
        default=True
    )
    class Meta:
        db_table = 'roles'
    def __str__(self):
        return self.role_name
class Permission(models.Model):
    permission_id = models.AutoField(
        primary_key=True
    )
    permission_name = models.CharField(
        max_length=100,
        unique=True
    )
    description = models.TextField()
    class Meta:
        db_table = 'permissions'
    def __str__(self):
        return self.permission_name
class User(AbstractUser):

    user_id = models.AutoField(
        primary_key=True
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='role_id'
    )
    mobile = models.CharField(
        max_length=15,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        default='Active'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = 'users'


class UserRole(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'user_roles'


class RolePermission(models.Model):

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE
    )

    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'role_permissions'


class AuditLog(models.Model):

    log_id = models.AutoField(
        primary_key=True
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    action = models.CharField(
        max_length=255
    )

    ip_address = models.GenericIPAddressField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = 'audit_logs'
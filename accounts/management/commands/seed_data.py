from django.core.management.base import BaseCommand

from faker import Faker

import random

from accounts.models import (
    User,
    Role,
    Permission,
    AuditLog
)

fake = Faker()


class Command(BaseCommand):

    help = 'Seed database with fake data'

    def handle(self, *args, **kwargs):

        self.stdout.write(
            self.style.SUCCESS(
                'Seeding data...'
            )
        )

        # -------------------------
        # Roles
        # -------------------------

        roles = [

            'Super Admin',
            'System Admin',
            'Manager',
            'QA'

        ]

        role_objects = []

        for role_name in roles:

            role, created = Role.objects.get_or_create(

                role_name=role_name,

                defaults={

                    'description':
                    f'{role_name} role',

                    'is_active': True

                }

            )

            role_objects.append(role)

        # -------------------------
        # Permissions
        # -------------------------

        permissions = [

            'VIEW',
            'MODIFY',
            'AUTHORIZE'

        ]

        for permission_name in permissions:

            Permission.objects.get_or_create(

                permission_name=permission_name,

                defaults={

                    'description':
                    f'{permission_name} permission'

                }

            )

        # -------------------------
        # Users
        # -------------------------

        users = []

        for i in range(20):

            username = fake.user_name()

            user = User.objects.create_user(

                username=username,

                email=fake.email(),

                password='password123',

                first_name=fake.first_name(),

                last_name=fake.last_name(),

                mobile=fake.phone_number(),

                status='Active',

                role=random.choice(role_objects)

            )

            users.append(user)

        # -------------------------
        # Audit Logs
        # -------------------------

        actions = [

            'Login',
            'Logout',
            'Profile Updated',
            'Password Changed',
            'User Deleted',
            'User Created'

        ]

        for i in range(100):

            AuditLog.objects.create(

                user=random.choice(users),

                action=random.choice(actions),

                ip_address=fake.ipv4()

            )

        self.stdout.write(

            self.style.SUCCESS(
                'Database seeded successfully!'
            )

        )
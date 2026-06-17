from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User as DjangoUser
from inventori.models import User as CustomUser

class InventoriAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Query custom user by id_user, email, or nama
            custom_user = CustomUser.objects.filter(
                id_user=username
            ).first() or CustomUser.objects.filter(
                email=username
            ).first() or CustomUser.objects.filter(
                nama=username
            ).first()

            if custom_user and custom_user.password == password:
                # Get or create standard Django user
                django_user, created = DjangoUser.objects.get_or_create(
                    username=custom_user.id_user,
                    defaults={
                        "email": custom_user.email or "",
                        "first_name": custom_user.nama
                    }
                )
                # Attach custom attributes to this instance
                django_user.id_user = custom_user.id_user
                django_user.nama = custom_user.nama
                django_user.role = custom_user.role
                return django_user
        except Exception as e:
            return None
        return None

    def get_user(self, user_id):
        try:
            django_user = DjangoUser.objects.get(pk=user_id)
            # Find matching custom user
            custom_user = CustomUser.objects.filter(id_user=django_user.username).first()
            if custom_user:
                django_user.id_user = custom_user.id_user
                django_user.nama = custom_user.nama
                django_user.role = custom_user.role
            else:
                first_custom = CustomUser.objects.filter(role__iexact="HC").first() or CustomUser.objects.first()
                django_user.id_user = first_custom.id_user if first_custom else django_user.username
                django_user.nama = django_user.first_name or django_user.username
                django_user.role = "HC" if django_user.is_superuser else "Employee"
            return django_user
        except DjangoUser.DoesNotExist:
            return None

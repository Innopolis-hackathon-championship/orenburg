from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, **extra_fields):
        user = self.model(**extra_fields)
        
        user.set_password(username)
        user.save()

        return user

    def create_superuser(self, username, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(username, **extra_fields)

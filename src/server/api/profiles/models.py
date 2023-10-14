from __future__ import annotations
from django.db import models
from django.utils import timezone
from django.core import validators
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from . managers import UserManager


class UserModel(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        "TG username", unique=True,
        max_length=127
    )
    fullname = models.CharField(
        "Полное имя", max_length=127,
        default=""
    )
    
    telegram_id = models.CharField(
        "telegram id", unique=True,
        max_length=127
    )

    balance = models.FloatField(
        "Баланс", default=0
    )
    class RoleChoices(models.TextChoices):
        BARMAID = "barmaid", "Повариха"
        COURIER = "courier", "Курьер"
        CUSTOMER = "customer", "Клиент"
        ADMIN = "admin", "Администратор"
        
    role = models.CharField(
        "Роль", max_length=10,
        choices=RoleChoices.choices,
        default=RoleChoices.CUSTOMER
    )
    
    joined = models.DateTimeField(
        "Дата регистрации", default=timezone.now
    )

    is_active = models.BooleanField(
        "Активный", default=True, help_text="Пользователь может авторизироваться"
    )
    is_superuser = models.BooleanField(
        "Администратор",
        default=False
    )
    
    is_confirmed = models.BooleanField(
        "is_confirmed", 
        default=False
    )
    
    code = models.CharField("code", max_length=50, default="")
    
    def verify(self, code: str) -> bool:
        """Verify user.

        Args:
            code (str): code, that user get from administrator.
        """
        if self.is_verified:
            return True
        if self.code != code:
            return False
        self.is_verified = True
        self.save()
        return True

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def cart(self):
        return CartModel.objects.filter(
            user_model=self
        ).all()
        
    @property
    def role_model(self):
        return role_model_map[self.role].objects.filter(
            user=self
        ).first()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "user"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return f"{self.username} {self.fullname}"

    def save(self, *args, **kwargs) -> UserModel:
        return super(UserModel, self).save(*args, **kwargs)


class CartModel(models.Model):
    user = models.ForeignKey(
        UserModel, models.CASCADE,
        verbose_name="Пользователь"
    )
    product = ...
    quantity = models.IntegerField(
        "Количество", default=1
    )
    
    class Meta:
        db_table = "profile__cart"
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
    
    def __str__(self) -> str:
        return f"{self.user.fullname} -> {self.product} ({self.quantity})"


class CourierModel(models.Model):
    user = models.OneToOneField(
        UserModel, models.CASCADE,
        verbose_name="Пользователь"
    )
    is_online = models.BooleanField(
        "На линии?", default=False
    )
    raiting = models.IntegerField(
        "Рейтинг", default=5,
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(5)
        ]
    )
    
    class Meta:
        db_table = "profile__courier"
        verbose_name = "Курьер"
        verbose_name_plural = "Курьеры"
        
    def __str__(self) -> str:
        return f"{self.user.username} ({self.raiting}) status: {self.is_online}"


class CustomerModel(models.Model):
    user = models.OneToOneField(
        UserModel, models.CASCADE,
        verbose_name="Пользователь"
    )

    class Meta:
        db_table = "profile__customer"
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        
    def __str__(self) -> str:
        return f"{self.user.username}"


class BarmaidModel(models.Model):
    user = models.OneToOneField(
        UserModel, models.CASCADE,
        verbose_name="Пользователь"
    )

    class Meta:
        db_table = "profile__barmaid"
        verbose_name = "Буфетчица"
        verbose_name_plural = "Буфетчицы"

    def __str__(self) -> str:
        return f"{self.user.username}"


class AdminModel(models.Model):
    @property
    def unverified_users(self):
        return UserModel.objects.filter(
            is_verified=False
        ).all()


role_model_map: dict[str, models.Model] = {
    UserModel.RoleChoices.CUSTOMER[0]: CustomerModel,
    UserModel.RoleChoices.BARMAID[0]: BarmaidModel,
    UserModel.RoleChoices.COURIER[0]: CourierModel,
}


@receiver(models.signals.post_save, sender=UserModel.role)
def update_user(sender, **kwargs):
    print(**kwargs)

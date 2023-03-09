from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Holder(models.Model):
    name = models.CharField(max_length=255, validators=[MinLengthValidator(2)])


class CreditCard(models.Model):
    exp_date = models.DateField()
    number = models.CharField(max_length=255)
    cvv = models.CharField(max_length=4, validators=[MinLengthValidator(3)])
    holder = models.ForeignKey(Holder, on_delete=models.CASCADE)
    brand = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.brand} ending with {self.number[-4:]}'


class UserRole(models.TextChoices):
    ADMIN = 'ADMIN', 'Admin'
    NON_ADMIN = 'NON_ADMIN', 'Non-Admin'


class UserManager(BaseUserManager):
    def create_user(self, name, password, role):
        if not name:
            raise ValueError('Users must have a name.')
        if not role:
            raise ValueError('Users must have a role.')
        user = self.model(
            name=name,
            role=role,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password):
        user = self.create_user(
            name=name,
            password=password,
            role=UserRole.ADMIN,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    name = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=UserRole.choices)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

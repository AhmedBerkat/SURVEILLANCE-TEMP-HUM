from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.timezone import now ,localtime
from django.utils import timezone
# Create your models here.
from django.db import models

class Dht11(models.Model):
  temp = models.FloatField(null=True)
  hum = models.FloatField(null=True)
  dt = models.DateTimeField(auto_now_add=True,null=True)


class BaseModel(models.Model):
    """Classe de base pour ajouter des champs communs à tous les modèles."""
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def create_user(self, type_user, password=None, **extra_fields):
        user = self.model(type_user=type_user, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    ROLE_CHOICES = [
        ('visiteur', 'Visiteur'),
        ('admin', 'Administrateur'),
    ]

    type_user = models.CharField(max_length=50, unique=True, choices=ROLE_CHOICES,primary_key=True )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'type_user'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.type_user
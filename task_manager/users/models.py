from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    identifier = models.CharField(max_length=40, unique=True, default='default_identifier')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'identifier'

    def __str__(self):
        """Represent model object."""
        return self.get_full_name
    
    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.identifier

    def get_short_name(self):
        return self.first_name or self.identifier

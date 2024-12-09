from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class User(AbstractBaseUser):

    def __str__(self):
        """Represent model object."""
        return self.get_full_name
# from django.contrib.auth.base_user import AbstractBaseUser
# from django.contrib.auth.models import PermissionsMixin, UserManager, Group, Permission
# from django.core.validators import MinLengthValidator
# from django.db import models
# from django.utils.translation import gettext_lazy as _
#
#
# class User(AbstractBaseUser, PermissionsMixin):
#
#     username = models.CharField(_("username"), max_length=50, unique=True,
#                                 error_messages={"unique": _("A user with that username already exists."), })
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     first_name = models.CharField(_("first name"), max_length=40, validators=[MinLengthValidator(2)],)
#     last_name = models.CharField(_("last name"), max_length=40, validators=[MinLengthValidator(2)],)
#     email = models.EmailField(_("email address"), max_length=150, unique=True)
#     phone = models.CharField(max_length=75, null=True, blank=True)
#     date_joined = models.DateTimeField(name="registered", auto_now_add=True)
#     last_login = models.DateTimeField(null=True, blank=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     deleted_at = models.DateTimeField(null=True, blank=True)
#     deleted = models.BooleanField(default=False)
#     # groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
#     # user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions_set', blank=True)
#
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["username", "first_name", "last_name"]
#
#     objects = UserManager()
#
#     def __str__(self):
#         return f"{self.last_name} {self.first_name}"
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE,  related_name='profile')
    description = models.TextField(blank=True, null=True)
    landlord = models.BooleanField(null=True)
    tenant = models.BooleanField(null=True)

    def __str__(self):
        return self.user.username
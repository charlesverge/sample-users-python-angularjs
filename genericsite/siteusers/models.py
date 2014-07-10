from uuidfield import UUIDField
import datetime
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models

class SiteUser(models.Model):
    """SiteUser is where users are stored, email and password's are used for login detials"""
    uuid = UUIDField(auto=True,primary_key=True)
    first_name = models.CharField(max_length=200, blank=False, error_messages={'blank': 'First name is required', 'invalid': 'The first name is invalid'})
    last_name = models.CharField(max_length=200, blank=False, error_messages={'blank': 'Last name is required', 'invalid': 'The last name is invalid'})
    email = models.EmailField(blank=False,unique=True)
    password = models.CharField(max_length=32, blank=False)
    created = models.DateTimeField(auto_now_add=True, blank=False, null=False)


from django.contrib import admin

# Register your models here.
from siteusers.models import SiteUser

admin.site.register(SiteUser)

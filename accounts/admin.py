from django.contrib import admin
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from .models import UserProfile, Company, Invitation
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Company)
admin.site.register(Invitation)
admin.site.register(EmailConfirmation)

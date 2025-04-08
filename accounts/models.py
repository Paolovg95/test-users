
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.

def age_validator(age):
    if age < 18:
        raise ValidationError('Age must be at least 18', params={'age': age})
class Company(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100, blank=True, null=True)
    admin = models.OneToOneField(User, on_delete = models.CASCADE, blank=True)
    class Meta():
        verbose_name_plural = "Companies"

class UserProfile(models.Model):
    # Create a one-to-one relationship between the UserProfile and the User
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    first_name = models.CharField(max_length=5)
    last_name = models.CharField(max_length=5)
    age = models.IntegerField(validators=[age_validator], blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return f"{self.user.username}"

class Invitation(models.Model):
    key = models.CharField(verbose_name=("Key"), max_length=64, unique=True, blank=True)
    accepted = models.BooleanField(verbose_name=("Accepted"),default=False, blank=True)
    sent = models.DateTimeField(verbose_name=("Sent"),default=timezone.now)
    created = models.DateTimeField(verbose_name=("Created"), default=timezone.now)
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField()

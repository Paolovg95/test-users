from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Company

class CustomSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email','password1', 'password2')
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self['email'].label = 'Correo Electrónico'
        # self['first_name'].label = 'Nombre'
        # self['last_name'].label = 'Apellido'
        self['password1'].label = 'Contraseña'
        self['password2'].label = 'Confirmar Contraseña'
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'age']
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'address']
    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        self['name'].label = 'Nombre Empresa'
        self['address'].label = 'Dirección de la Empresa'
class SendInviteForm(forms.Form):
    email = forms.EmailField()

from django import forms
from .models import CashFlow, Asset, Liability
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class CashFlowForm(forms.ModelForm):
    class Meta:
        model = CashFlow
        fields = ['date', 'amount']


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'amount']


class LiabilityForm(forms.ModelForm):
    class Meta:
        model = Liability
        fields = ['name', 'amount']


class RegistrationForm(UserCreationForm):
    # Add any additional fields or customization here
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'bio', 'profile_picture']



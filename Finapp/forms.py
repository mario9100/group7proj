from django import forms
from .models import Asset, Liability, UserProfile, Income, Expense
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Questionnaire


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


class QuestionnaireForm(forms.Form):

    EXPERIENCE_CHOICES = [
        ('<1', 'Less than 1 year'),
        ('1-2', '1-2 years'),
        ('3-5', '3-5 years'),
        ('6-10', '6-10 years'),
        ('10+', 'More than 10 years'),
    ]
    experience = forms.ChoiceField(choices=EXPERIENCE_CHOICES, label="Investment Experience")

    RISK_TOLERANCE_CHOICES = [
        (1, 'Strongly Disagree'),
        (2, 'Disagree'),
        (3, 'Agree'),
        (4, 'Strongly Agree'),
    ]
    question_1 = forms.ChoiceField(choices=RISK_TOLERANCE_CHOICES,
                                   label="I am comfortable with investments that may fluctuate in value.",
                                   widget=forms.RadioSelect)
    question_2 = forms.ChoiceField(choices=RISK_TOLERANCE_CHOICES,
                                   label="I prefer investments with little or no risk even if it means lower returns.",
                                   widget=forms.RadioSelect)
    question_3 = forms.ChoiceField(choices=RISK_TOLERANCE_CHOICES,
                                   label="I am willing to take on high risk for the chance of high returns.",
                                   widget=forms.RadioSelect)


    def clean(self):
        cleaned_data = super().clean()

        total_score = sum([int(cleaned_data.get(f"question_{i + 1}", 0)) for i in range(3)])

        if total_score <= 6:
            risk_profile = 'Conservative'
        elif 7 <= total_score <= 9:
            risk_profile = 'Moderate'
        else:
            risk_profile = 'Aggressive'


        self.cleaned_data['risk_profile'] = risk_profile

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['name', 'net_income']


class ExpenseForm(forms.ModelForm):

    EXPENSE_TYPE_CHOICES = [
        ('Living', 'Living Expense'),
        ('Discretionary', 'Discretionary Expense'),
    ]


    expense_type = forms.ChoiceField(choices=EXPENSE_TYPE_CHOICES, label="Type of Expense")

    class Meta:
        model = Expense
        fields = ['name', 'amount', 'expense_type']

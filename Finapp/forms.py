from django import forms
from .models import CashFlow, Asset, Liability
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Questionnaire
from .models import Income, Expense

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


class QuestionnaireForm(forms.Form):
    # Experience dropdown
    EXPERIENCE_CHOICES = [
        ('<1', 'Less than 1 year'),
        ('1-2', '1-2 years'),
        ('3-5', '3-5 years'),
        ('6-10', '6-10 years'),
        ('10+', 'More than 10 years'),
    ]
    experience = forms.ChoiceField(choices=EXPERIENCE_CHOICES, label="Investment Experience")

    # Risk tolerance questions
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

    # Add more questions as needed...

    def clean(self):
        cleaned_data = super().clean()
        # Convert each value to int before summing
        total_score = sum([int(cleaned_data.get(f"question_{i + 1}", 0)) for i in range(3)])
        # Rest of your code...
        # Adjust the range for the number of questions
        # Determine risk profile based on the total score
        if total_score <= 6:
            risk_profile = 'Conservative'
        elif 7 <= total_score <= 9:
            risk_profile = 'Moderate'
        else:
            risk_profile = 'Aggressive'

        # You can then use this to save the profile to the user or simply pass it to the context
        self.cleaned_data['risk_profile'] = risk_profile

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['name', 'net_income']  # Adjust the fields as per your Income model


class ExpenseForm(forms.ModelForm):
    # Define the choices for expense type
    EXPENSE_TYPE_CHOICES = [
        ('Living', 'Living Expense'),
        ('Discretionary', 'Discretionary Expense'),
    ]

    # Add an extra field for the expense type with the choices
    expense_type = forms.ChoiceField(choices=EXPENSE_TYPE_CHOICES, label="Type of Expense")

    class Meta:
        model = Expense
        fields = ['name', 'amount', 'expense_type']  # Include other fields if needed

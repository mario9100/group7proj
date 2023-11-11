from django.shortcuts import render, redirect
from .forms import AssetForm, LiabilityForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import RegistrationForm
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from .models import Asset, Liability, CashFlow
from django.contrib import messages
from django.db import models
from .forms import QuestionnaireForm, IncomeForm, ExpenseForm
from .models import RiskProfile
from .models import Income, Expense
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Sum

def success(request):
    return render(request, 'Finapp/success.html')

@login_required
def import_asset(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.user = request.user  # Set the user field
            asset.save()  # Now save the asset
            messages.success(request, 'Asset imported successfully!')
            return redirect('Finapp:dashboard')

    else:
        form = AssetForm()

    return render(request, 'Finapp/import_asset.html', {'form': form})

@login_required
def import_liability(request):
    if request.method == 'POST':
        form = LiabilityForm(request.POST)
        if form.is_valid():
            liability = form.save(commit=False)
            liability.user = request.user  # Set the user field
            liability.save()  # Now save the liability
            messages.success(request, 'Liability imported successfully!')
            return redirect('Finapp:dashboard')

    else:
        form = LiabilityForm()

    return render(request, 'Finapp/import_liability.html', {'form': form})

def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or login page
            return redirect('login')  # Assuming you have a 'login' URL pattern
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def view_profile(request):
    # Retrieve the user's profile (assuming you have a one-to-one relationship with User)
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    return render(request, 'profile/view_profile.html', {'user_profile': user_profile})


@login_required
def edit_profile(request):
    # Retrieve the user's profile (assuming you have a one-to-one relationship with User)
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('Finapp:view_profile')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'profile/edit_profile.html', {'form': form})

# views.py


@login_required
def dashboard(request):
    assets = Asset.objects.filter(user=request.user)
    liabilities = Liability.objects.filter(user=request.user)
    cash_flows = CashFlow.objects.filter(user=request.user)
    user_profile = UserProfile.objects.get(user=request.user)  # Get the user profile
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)

    total_assets = assets.aggregate(total=Sum('amount'))['total'] or 0
    total_liabilities = liabilities.aggregate(total=Sum('amount'))['total'] or 0
    total_incomes = incomes.aggregate(total=Sum('net_income'))['total'] or 0
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
    net_cash_flows = total_incomes - total_expenses
    net_worth = total_assets - total_liabilities

    context = {
        'assets': assets,
        'liabilities': liabilities,
        'cash_flows': cash_flows,  # This may need to be adjusted based on what you store in CashFlow
        'net_worth': net_worth,
        'net_cash_flows': net_cash_flows,  # Added this line
        'risk_profile': user_profile.risk_profile if user_profile else None,
        'incomes': incomes,
        'expenses': expenses,
    }
    return render(request, 'Finapp/dashboard.html', context)

@login_required
@login_required
def questionnaire_view(request):
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            # The risk profile is calculated and added to cleaned_data in the form's clean method
            risk_profile = form.cleaned_data['risk_profile']

            # Save the risk profile to the user's profile
            user_profile = request.user.userprofile
            user_profile.risk_profile = risk_profile
            user_profile.save()

            # Redirect to the dashboard where the user can see their risk profile
            return redirect('Finapp:dashboard')
        else:
            # If the form is not valid, you might want to return the form with errors
            return render(request, 'questionnaire.html', {'form': form})
    else:
        form = QuestionnaireForm()

    # If GET request, just display the empty form
    return render(request, 'questionnaire.html', {'form': form})


def determine_risk_profile(data):
    # Example logic for determining risk profile
    experience = data['experience']
    tolerance = data['risk_tolerance']
    if experience > 5 and tolerance == 'high':
        return RiskProfile.objects.get(profile_name='Aggressive')
    elif experience <= 5 and tolerance == 'low':
        return RiskProfile.objects.get(profile_name='Conservative')
    else:
        return RiskProfile.objects.get(profile_name='Moderate')

# views.py

@login_required
def import_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('Finapp:dashboard')
    else:
        form = IncomeForm()
    return render(request, 'Finapp/import_income.html', {'form': form})

@login_required
def import_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            # Save the expense with the user and type
            expense = form.save(commit=False)
            expense.user = request.user
            expense.expense_type = form.cleaned_data['expense_type']
            expense.save()
            # Redirect to a new URL:
            return redirect('Finapp:dashboard')  # Update with your actual redirect destination

    else:
        form = ExpenseForm()

    return render(request, 'Finapp/import_expense.html', {'form': form})

@login_required
def delete_object(request, object_id, model, redirect_url):
    obj = get_object_or_404(model, id=object_id, user=request.user)
    obj.delete()
    return redirect(redirect_url)

# Now, your specific delete views can call this generic function:
@login_required
def delete_asset(request, asset_id):
    return delete_object(request, asset_id, Asset, 'Finapp:dashboard')

@login_required
def delete_liability(request, liability_id):
    return delete_object(request, liability_id, Liability, 'Finapp:dashboard')

@login_required
def delete_income(request, income_id):
    return delete_object(request, income_id, Income, 'Finapp:dashboard')

@login_required
def delete_expense(request, expense_id):
    return delete_object(request, expense_id, Expense, 'Finapp:dashboard')

@login_required
def delete_cash_flow(request, cash_flow_id):
    return delete_object(request, cash_flow_id, Cash_flow, 'Finapp:dashboard')

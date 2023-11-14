from .forms import AssetForm, LiabilityForm, RegistrationForm, UserProfileForm, QuestionnaireForm, IncomeForm, ExpenseForm
from .models import UserProfile, Asset, Liability, RiskProfile, Income, Expense
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
import requests
from decouple import config

def success(request):
    return render(request, 'success.html')

@login_required
def import_asset(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.user = request.user
            asset.save()
            messages.success(request, 'Asset imported successfully!')
            return redirect('Finapp:dashboard')

    else:
        form = AssetForm()

    return render(request, 'import_asset.html', {'form': form})

@login_required
def import_liability(request):
    if request.method == 'POST':
        form = LiabilityForm(request.POST)
        if form.is_valid():
            liability = form.save(commit=False)
            liability.user = request.user
            liability.save()
            messages.success(request, 'Liability imported successfully!')
            return redirect('Finapp:dashboard')

    else:
        form = LiabilityForm()

    return render(request, 'import_liability.html', {'form': form})

def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Finapp:login')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def view_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    return render(request, 'view_profile.html', {'user_profile': user_profile})


@login_required
def edit_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('Finapp:view_profile')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'edit_profile.html', {'form': form})

# views.py


@login_required
def dashboard(request):
    assets = Asset.objects.filter(user=request.user)
    liabilities = Liability.objects.filter(user=request.user)
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
        'net_worth': net_worth,
        'net_cash_flows': net_cash_flows,  # Added this line
        'risk_profile': user_profile.risk_profile if user_profile else None,
        'incomes': incomes,
        'expenses': expenses,
    }
    return render(request, 'dashboard.html', context)


@login_required
def questionnaire_view(request):
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            risk_profile = form.cleaned_data['risk_profile']

            user_profile = request.user.userprofile
            user_profile.risk_profile = risk_profile
            user_profile.save()

            return redirect('Finapp:dashboard')
        else:
            return render(request, 'questionnaire.html', {'form': form})
    else:
        form = QuestionnaireForm()
    return render(request, 'questionnaire.html', {'form': form})


def determine_risk_profile(data):
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
    return render(request, 'import_income.html', {'form': form})

@login_required
def import_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.expense_type = form.cleaned_data['expense_type']
            expense.save()
            # Redirect to a new URL:
            return redirect('Finapp:dashboard')

    else:
        form = ExpenseForm()

    return render(request, 'import_expense.html', {'form': form})

@login_required
def delete_object(request, object_id, model, redirect_url):
    obj = get_object_or_404(model, id=object_id, user=request.user)
    obj.delete()
    return redirect(redirect_url)

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

def fetch_financial_news():
    url = "https://newsapi.org/v2/everything"
    parameters = {
        'q': 'finance',
        'sortBy': 'popularity',
        'apiKey': config('NEWS_API_KEY'),
        'language': 'en',
    }
    try:
        response = requests.get(url, params=parameters)
        response.raise_for_status()
        return response.json()['articles']
    except requests.exceptions.RequestException as e:

        print(f"Request failed: {e}")
        return None

def financial_news_view(request):
    financial_news = fetch_financial_news()
    if financial_news:
        return render(request, 'financial_news.html', {'financial_news': financial_news})
    else:
        return render(request, 'financial_news.html', {'error': 'Unable to fetch financial news'})

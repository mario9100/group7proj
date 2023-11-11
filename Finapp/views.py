from django.shortcuts import render, redirect
from .forms import CashFlowForm, AssetForm, LiabilityForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import RegistrationForm
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from .models import Asset, Liability, CashFlow
from django.contrib import messages
from django.db import models
from .forms import QuestionnaireForm
from .models import RiskProfile
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

@login_required
def import_cash_flow(request):
    if request.method == 'POST':
        form = CashFlowForm(request.POST)
        if form.is_valid():
            cash_flow = form.save(commit=False)
            cash_flow.user = request.user  # Set the user field
            cash_flow.save()  # Now save the cash_flow
            messages.success(request, 'Cash Flow imported successfully!')
            return redirect('Finapp:dashboard')

    else:
        form = CashFlowForm()

    return render(request, 'Finapp/import_cash_flow.html', {'form': form})


# ... rest of your views ...
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

    total_assets = assets.aggregate(total=models.Sum('amount'))['total'] or 0
    total_liabilities = liabilities.aggregate(total=models.Sum('amount'))['total'] or 0
    net_worth = total_assets - total_liabilities

    context = {
        'assets': assets,
        'liabilities': liabilities,
        'cash_flows': cash_flows,
        'net_worth': net_worth,
        'risk_profile': user_profile.risk_profile,  # Add the risk profile to the context
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

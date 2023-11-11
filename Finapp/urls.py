from django.urls import path, include
from . import views  # Import views from your app
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from .views import questionnaire_view

app_name = 'Finapp'

urlpatterns = [
    # Define URL patterns and associate them with view functions.
    path('import_cash_flow/', views.import_cash_flow, name='import_cash_flow'),
    path('import_asset/', views.import_asset, name='import_asset'),
    path('import_liability/', views.import_liability, name='import_liability'),
    path('success/', views.success, name='success'),
    path('register/', views.registration_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile_alt'),  # Updated name
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('questionnaire/', questionnaire_view, name='questionnaire'),
    # Add more URL patterns as needed.
]

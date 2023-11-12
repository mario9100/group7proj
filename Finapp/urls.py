from django.urls import path, include
from . import views  # Import views from your app
from django.contrib.auth import views as auth_views
from .views import questionnaire_view, delete_asset, delete_liability, delete_income, delete_expense

app_name = 'Finapp'

urlpatterns = [
    path('import_asset/', views.import_asset, name='import_asset'),
    path('import_liability/', views.import_liability, name='import_liability'),
    path('success/', views.success, name='success'),
    path('register/', views.registration_view, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile_alt'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('questionnaire/', questionnaire_view, name='questionnaire'),
    path('import_income/', views.import_income, name='import_income'),
    path('import_expense/', views.import_expense, name='import_expense'),
    path('delete_asset/<int:asset_id>/', delete_asset, name='delete_asset'),
    path('delete_liability/<int:liability_id>/', delete_liability, name='delete_liability'),
    path('delete_income/<int:income_id>/', delete_income, name='delete_income'),
    path('delete_expense/<int:expense_id>/', delete_expense, name='delete_expense'),
    path('financial_news/', views.financial_news_view, name='financial_news'),
]

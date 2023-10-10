from django.contrib import admin
from .models import CashFlow, Asset, Liability
from .models import UserProfile


@admin.register(CashFlow)
class CashFlowAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount')
    list_filter = ('date',)
    search_fields = ('date', 'amount')


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount')
    search_fields = ('name', 'amount')


@admin.register(Liability)
class LiabilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount')
    search_fields = ('name', 'amount')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'bio')
    search_fields = ('user__username', 'full_name')

from django.contrib import admin
from .models import Asset, Liability
from .models import UserProfile


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

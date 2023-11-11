from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class CashFlow(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.date} - {self.amount} by {self.user.username}"

class Asset(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.name} - {self.amount} by {self.user.username}"

class Liability(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.name} - {self.amount} by {self.user.username}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    risk_profile = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()


class RiskProfile(models.Model):
    profile_name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.profile_name

class Questionnaire(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    investment_experience = models.IntegerField()  # For example, number of years
    risk_tolerance = models.CharField(max_length=10)  # For example: low, medium, high
    risk_profile = models.ForeignKey(RiskProfile, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Questionnaire for {self.user.username}"

# models.py

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='Misc Income')
    gross_income = models.DecimalField(max_digits=10, decimal_places=2)
    net_income = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Gross: {self.gross_income}, Net: {self.net_income}"

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='Misc Expense')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateField(auto_now_add=True)
    expense_type = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.user.username} - Living: {self.living_expenses}, Discretionary: {self.discretionary_expenses}"

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

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()

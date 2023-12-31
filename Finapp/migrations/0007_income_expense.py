# Generated by Django 4.2.5 on 2023-11-11 02:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Finapp', '0006_userprofile_risk_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gross_income', models.DecimalField(decimal_places=2, max_digits=10)),
                ('net_income', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('living_expenses', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discretionary_expenses', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

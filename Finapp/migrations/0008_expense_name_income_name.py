# Generated by Django 4.2.5 on 2023-11-11 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Finapp', '0007_income_expense'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='name',
            field=models.CharField(default='Misc Expense', max_length=100),
        ),
        migrations.AddField(
            model_name='income',
            name='name',
            field=models.CharField(default='Misc Income', max_length=100),
        ),
    ]

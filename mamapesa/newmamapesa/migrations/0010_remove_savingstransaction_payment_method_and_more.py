# Generated by Django 5.0.2 on 2024-03-08 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newmamapesa', '0009_currency_remove_userdetails_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='savingstransaction',
            name='payment_method',
        ),
        migrations.RemoveField(
            model_name='savingstransaction',
            name='savings_item',
        ),
        migrations.DeleteModel(
            name='LoanTransaction',
        ),
        migrations.DeleteModel(
            name='SavingsTransaction',
        ),
    ]

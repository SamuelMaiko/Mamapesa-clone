# Generated by Django 5.0.2 on 2024-03-05 17:25

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newmamapesa', '0017_alter_savings_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='idnumber',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='interest_rate',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='loan_limit',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='phonenumber',
        ),
        migrations.RemoveField(
            model_name='loan',
            name='due_date',
        ),
        migrations.RemoveField(
            model_name='loan',
            name='overdue_rate',
        ),
        migrations.RemoveField(
            model_name='loan',
            name='repayments',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(default='example@example.com', max_length=254, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='duration_months',
            field=models.IntegerField(default=12),
        ),
        migrations.AlterField(
            model_name='trustscore',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='withdrawal',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.CreateModel(
            name='LoanPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('description', models.TextField(blank=True, null=True)),
                ('payment_method', models.CharField(blank=True, max_length=50, null=True)),
                ('reference_number', models.CharField(blank=True, max_length=50, null=True)),
                ('is_successful', models.BooleanField(default=True)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='newmamapesa.loan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loan_payments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SavingsPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('description', models.TextField(blank=True, null=True)),
                ('payment_method', models.CharField(blank=True, max_length=50, null=True)),
                ('reference_number', models.CharField(blank=True, max_length=50, null=True)),
                ('is_successful', models.BooleanField(default=True)),
                ('savings', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='all_payments', to='newmamapesa.savings')),
                ('savings_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_payments', to='newmamapesa.savingsitem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='savings_payments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
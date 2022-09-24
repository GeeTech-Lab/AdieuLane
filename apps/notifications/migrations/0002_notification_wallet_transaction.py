# Generated by Django 3.2.15 on 2022-09-23 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('notifications', '0001_initial'),
        ('wallets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='wallet_transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wallet_transaction_notifications', to='wallets.wallettransaction'),
        ),
    ]

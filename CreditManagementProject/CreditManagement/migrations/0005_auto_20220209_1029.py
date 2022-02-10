# Generated by Django 3.0.7 on 2022-02-09 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CreditManagement', '0004_alter_ledger_store_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distributor',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='ledger',
            name='credit_rating',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='ledger',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='ledger_action_types',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='ledger_actions',
            name='current_value',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='ledger_actions',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='ledger_actions',
            name='prev_value',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='ledger_transactions',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='store',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]

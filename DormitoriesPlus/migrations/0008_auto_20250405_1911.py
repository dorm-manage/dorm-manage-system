# Generated by Django 3.1.12 on 2025-04-05 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DormitoriesPlus', '0007_auto_20250405_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='fault_type',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='סוג התקלה'),
        ),
        migrations.AddField(
            model_name='request',
            name='urgency',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='דחיפות'),
        ),
    ]


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DormitoriesPlus', '0005_request_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='admin_note',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='הערות מנהל'),
        ),
        migrations.AddField(
            model_name='request',
            name='return_date',
            field=models.DateField(blank=True, null=True, verbose_name='תאריך החזרה מתוכנן'),
        ),
    ]
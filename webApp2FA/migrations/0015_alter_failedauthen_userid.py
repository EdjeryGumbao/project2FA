# Generated by Django 4.2.3 on 2023-08-22 10:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webApp2FA', '0014_alter_failedauthen_failedauthenimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='failedauthen',
            name='userID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

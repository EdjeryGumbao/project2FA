# Generated by Django 4.2.3 on 2023-08-04 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webApp2FA', '0008_rename_url_websitelist_websiteurl'),
    ]

    operations = [
        migrations.DeleteModel(
            name='IntruderImage',
        ),
    ]

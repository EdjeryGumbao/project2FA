# Generated by Django 4.2.3 on 2023-08-04 06:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webApp2FA', '0003_rename_user_userimage_userid_alter_userimage_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userimage',
            old_name='image',
            new_name='userImage',
        ),
        migrations.CreateModel(
            name='IntuderImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intruderImage', models.ImageField(blank=True, null=True, upload_to='intruderimages/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('userID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

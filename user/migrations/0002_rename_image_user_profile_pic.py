# Generated by Django 5.0.3 on 2024-03-13 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='image',
            new_name='profile_pic',
        ),
    ]

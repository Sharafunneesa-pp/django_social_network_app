# Generated by Django 5.0 on 2023-12-30 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0005_userprofile_followiings'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='followiings',
            new_name='followings',
        ),
    ]

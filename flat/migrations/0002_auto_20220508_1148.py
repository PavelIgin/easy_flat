# Generated by Django 3.1 on 2022-05-08 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flat',
            old_name='arena_timeline',
            new_name='rent_timeline',
        ),
    ]
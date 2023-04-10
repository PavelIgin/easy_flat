# Generated by Django 3.1 on 2022-05-02 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flat', '0005_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flat',
            old_name='date_publish',
            new_name='date_publisher',
        ),
        migrations.AddField(
            model_name='flat',
            name='photos',
            field=models.ImageField(blank=True, null=True, upload_to='flat_images'),
        ),
    ]

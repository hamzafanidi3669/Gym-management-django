# Generated by Django 4.2.13 on 2024-07-01 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0012_alter_customuser_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='photo_couverture',
            field=models.ImageField(null=True, upload_to='uploads/profile/photo_couverture'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='photo_profil',
            field=models.ImageField(null=True, upload_to='uploads/profile/photo_profil'),
        ),
    ]

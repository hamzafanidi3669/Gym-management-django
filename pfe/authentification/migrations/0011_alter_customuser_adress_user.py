# Generated by Django 4.2.13 on 2024-06-19 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0010_alter_customuser_adress_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='adress_user',
            field=models.CharField(blank=True, default='', max_length=150, verbose_name='Adresse'),
        ),
    ]

# Generated by Django 4.2.13 on 2024-07-24 22:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0006_post_media_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservationSeance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_debut', models.DateTimeField()),
                ('date_fin', models.DateTimeField()),
                ('statut', models.CharField(choices=[('reservee', 'Réservée'), ('annulee', 'Annulée'), ('terminee', 'Terminée')], default='reservee', max_length=20)),
                ('commentaire', models.TextField(blank=True, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seances_client', to=settings.AUTH_USER_MODEL)),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seances_coach', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Réservation de séance',
                'verbose_name_plural': 'Réservations de séances',
                'ordering': ['date_debut'],
            },
        ),
    ]
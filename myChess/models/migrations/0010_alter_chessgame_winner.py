# Generated by Django 4.2.2 on 2024-04-09 21:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0009_alter_chessgame_blackplayer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chessgame',
            name='winner',
            field=models.ForeignKey(blank=True, help_text='El ganador de la partida.Puede ser nulo si el juego está pendiente o ha terminado en empate.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='games_won', to=settings.AUTH_USER_MODEL),
        ),
    ]
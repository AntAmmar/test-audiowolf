# Generated by Django 3.2.12 on 2022-02-24 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adverts', '0004_advertvideostatus_spotify_get_tracks'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertvideostatus',
            name='send_acr_cloud',
            field=models.CharField(choices=[('NOT_STARTED', 'Not started'), ('IN_PROGRESS', 'In progress'), ('SUCCESS', 'Successfully finished'), ('ERROR', 'Error')], default='NOT_STARTED', max_length=100),
        ),
    ]

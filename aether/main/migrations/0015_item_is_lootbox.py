# Generated by Django 5.0.8 on 2024-09-06 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_event_event_photo_seasonalcontent_sc_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='is_lootbox',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 2.2.6 on 2019-11-11 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cardsite', '0019_usedcard'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='final_cards',
            field=models.ManyToManyField(blank=True, to='cardsite.UsedCard'),
        ),
        migrations.AlterField(
            model_name='usedcard',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]

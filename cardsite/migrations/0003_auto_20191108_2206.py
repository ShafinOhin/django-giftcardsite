# Generated by Django 2.2.6 on 2019-11-08 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cardsite', '0002_auto_20191108_2144'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='test-product'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='catagory',
            field=models.CharField(choices=[('GP', 'Google Play'), ('AM', 'AMAZON'), ('NF', 'NETFLIX'), ('IT', 'ITUNES'), ('ST', 'STEAM')], max_length=2),
        ),
    ]

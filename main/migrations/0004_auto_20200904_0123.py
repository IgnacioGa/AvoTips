# Generated by Django 3.0.3 on 2020-09-04 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200904_0120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrera',
            name='relacionadas',
            field=models.ManyToManyField(blank=True, null=True, related_name='_carrera_relacionadas_+', to='main.Carrera'),
        ),
    ]

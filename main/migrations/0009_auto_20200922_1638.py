# Generated by Django 3.0.3 on 2020-09-22 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20200907_1935'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carrera',
            name='orientaciones',
        ),
        migrations.RemoveField(
            model_name='carrera',
            name='universidades',
        ),
        migrations.RemoveField(
            model_name='orientacion',
            name='informacion',
        ),
        migrations.AlterField(
            model_name='universidad',
            name='abreviacion',
            field=models.CharField(default='', max_length=8),
        ),
    ]

# Generated by Django 4.0.5 on 2022-06-25 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangogram', '0002_alter_duser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duser',
            name='avatar',
            field=models.ImageField(blank=True, default='default.png', upload_to='pics'),
        ),
    ]

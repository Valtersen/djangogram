# Generated by Django 4.0.5 on 2022-06-26 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangogram', '0012_alter_duser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duser',
            name='avatar',
            field=models.ImageField(default='default.png', null=True, upload_to='users/avatars/'),
        ),
    ]

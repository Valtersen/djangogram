# Generated by Django 4.0.5 on 2022-06-26 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangogram', '0006_post_postimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimage',
            name='image',
            field=models.ImageField(null=True, upload_to='posts/%Y/%m/%d'),
        ),
    ]

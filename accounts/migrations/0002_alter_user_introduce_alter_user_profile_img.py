# Generated by Django 4.2.11 on 2024-05-14 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='introduce',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_img',
            field=models.ImageField(upload_to='media\\profile'),
        ),
    ]

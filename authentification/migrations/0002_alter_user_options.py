# Generated by Django 4.2 on 2023-04-29 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('-created_at',)},
        ),
    ]
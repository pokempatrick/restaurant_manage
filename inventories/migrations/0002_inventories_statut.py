# Generated by Django 4.2 on 2023-05-11 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventories',
            name='statut',
            field=models.CharField(choices=[('CREATED', 'nouveau'), ('SUBMITTED', 'Soumis'), ('APPROVED', 'Validé'), ('REJECTED', 'rejeté')], default='CREATED', max_length=150),
        ),
    ]

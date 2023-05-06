# Generated by Django 4.2 on 2023-05-06 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0002_alter_user_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role_name',
            field=models.CharField(choices=[('ROLE_ADMIN', 'admin'), ('ROLE_SUPER_ADMIN', 'surper_admin'), ('ROLE_OWNER', 'Propriétaire'), ('ROLE_MANAGER', 'Gérant'), ('ROLE_ACCOUNTANT', 'Comptable'), ('ROLE_COOKER', 'Cuisinier'), ('ROLE_TECHNICIAN', 'Technicien'), ('ROLE_ANONYME', 'Anonyme')], default='ROLE_ANONYME', max_length=150, verbose_name='role name'),
        ),
    ]
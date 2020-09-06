# Generated by Django 3.1 on 2020-09-06 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='compte',
            old_name='addresse',
            new_name='adresse',
        ),
        migrations.AddField(
            model_name='compte',
            name='type_compte',
            field=models.CharField(blank=True, choices=[('Ge', 'Gerant'), ('Ag', 'Agence')], max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='compte',
            name='valide',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
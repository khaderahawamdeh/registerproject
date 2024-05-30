# Generated by Django 5.0.4 on 2024-05-30 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='prerequisites',
        ),
        migrations.AddField(
            model_name='course',
            name='prerequisites',
            field=models.ManyToManyField(blank=True, related_name='prerequisite_for', to='myapp.course'),
        ),
    ]

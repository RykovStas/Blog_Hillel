# Generated by Django 4.2.1 on 2023-05-10 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
    ]
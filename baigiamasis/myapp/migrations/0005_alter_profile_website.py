# Generated by Django 4.2.8 on 2023-12-11 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_profile_facebook_alter_profile_instagram'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='website',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]

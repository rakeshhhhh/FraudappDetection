# Generated by Django 4.0.4 on 2022-04-16 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_user_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_details',
            name='user_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]

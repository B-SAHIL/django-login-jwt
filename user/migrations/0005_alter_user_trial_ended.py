# Generated by Django 4.2.5 on 2023-09-20 14:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_user_native_name_remove_user_phone_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='trial_ended',
            field=models.DateField(default=datetime.date(2023, 10, 20)),
        ),
    ]
# Generated by Django 4.2.5 on 2023-09-20 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default=models.EmailField(default='', max_length=254, null=True, unique=True), max_length=191, unique=True),
        ),
    ]
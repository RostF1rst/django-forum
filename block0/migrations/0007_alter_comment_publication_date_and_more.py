# Generated by Django 4.2 on 2023-04-17 14:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('block0', '0006_alter_comment_publication_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='publication_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 17, 14, 54, 45, 837106, tzinfo=datetime.timezone.utc), verbose_name='date of publication'),
        ),
        migrations.AlterField(
            model_name='post',
            name='publication_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 17, 14, 54, 45, 837106, tzinfo=datetime.timezone.utc), verbose_name='date of publication'),
        ),
    ]
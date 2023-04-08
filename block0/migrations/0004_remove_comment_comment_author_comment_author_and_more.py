# Generated by Django 4.1.5 on 2023-04-01 16:48

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('block0', '0003_post_author_alter_comment_publication_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='comment_author',
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='publication_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 1, 16, 48, 23, 447781, tzinfo=datetime.timezone.utc), verbose_name='date of publication'),
        ),
        migrations.AlterField(
            model_name='post',
            name='publication_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 1, 16, 48, 23, 447412, tzinfo=datetime.timezone.utc), verbose_name='date of publication'),
        ),
    ]
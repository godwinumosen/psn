# Generated by Django 5.1.6 on 2025-03-26 08:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psnypg', '0005_logopicturepost'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExcosUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excos_user_name', models.CharField(max_length=255)),
                ('excos_user_description', models.TextField()),
                ('excos_user_slug', models.SlugField(blank=True, max_length=255, null=True)),
                ('excos_user_email', models.EmailField(max_length=255)),
                ('excos_user_whatsapp_number', models.CharField(max_length=15)),
                ('excos_user_url', models.URLField(blank=True, max_length=255, null=True)),
                ('excos_user_publish_date', models.DateTimeField(auto_now_add=True)),
                ('excos_user_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['excos_user_publish_date'],
            },
        ),
    ]

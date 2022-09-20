# Generated by Django 3.2.15 on 2022-09-20 16:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Diary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(choices=[('public', 'Public'), ('private', 'Private')], max_length=64, verbose_name='kind')),
                ('title', models.CharField(max_length=256, unique=True, verbose_name='title')),
                ('expiration', models.DateTimeField(blank=True, null=True, verbose_name='expiration')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diaries', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'diary',
                'verbose_name_plural': 'diaries',
            },
        ),
    ]

# Generated by Django 3.2.15 on 2022-09-20 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('diary', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='content')),
                ('diary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='diary.diary', verbose_name='diary')),
            ],
            options={
                'verbose_name': 'note',
                'verbose_name_plural': 'notes',
            },
        ),
    ]

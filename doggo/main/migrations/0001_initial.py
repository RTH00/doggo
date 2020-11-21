# Generated by Django 3.0.4 on 2020-03-28 21:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('id_secret', models.TextField(null=True)),
                ('created_at', models.DateTimeField(null=True)),
                ('last_seen_at', models.DateTimeField(null=True)),
                ('cookie_consent_at', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'accounts',
            },
        ),
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('id_public', models.TextField(null=True, unique=True)),
                ('created_at', models.DateTimeField(null=True)),
                ('name', models.TextField(null=True)),
                ('breed', models.TextField(default='GERMAN_SHEPHERD')),
                ('last_refresh', models.DateTimeField(null=True)),
                ('status', models.TextField(default='AVAILABLE')),
                ('status_set_at', models.DateTimeField(null=True)),
                ('food', models.FloatField(default=0.5)),
                ('fat', models.FloatField(default=0.0)),
                ('affection', models.FloatField(default=0.5)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Account')),
            ],
            options={
                'db_table': 'dogs',
            },
        ),
    ]

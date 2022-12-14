# Generated by Django 2.0 on 2021-04-20 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=220)),
                ('url', models.URLField()),
                ('breed', models.CharField(blank=True, max_length=220)),
                ('age', models.IntegerField(default=0)),
                ('gender', models.CharField(blank=True, max_length=220)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-28 03:48
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fixer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name="Fixer's name")),
                ('slug', autoslug.fields.AutoSlugField(editable=False, max_length=32, populate_from='name', unique=True)),
                ('image_url', models.URLField(blank=True, max_length=255)),
                ('rating', models.DecimalField(decimal_places=2, default=0, max_digits=3, verbose_name="Fixer's initial rating")),
            ],
        ),
        migrations.CreateModel(
            name='FixerRank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.FloatField(default=0.0)),
                ('fixer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='score', to='ranksearch.Fixer')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(default='')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True)),
                ('rating', models.PositiveIntegerField(default=1)),
                ('fixer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='ranksearch.Fixer')),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name="Owner's name")),
                ('slug', autoslug.fields.AutoSlugField(editable=False, max_length=32, populate_from='name', unique=True)),
                ('image_url', models.URLField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, max_length=32, populate_from='name', unique=True)),
                ('image_url', models.URLField(blank=True, max_length=255)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='ranksearch.Owner', verbose_name='Property')),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='properties',
            field=models.ManyToManyField(related_name='jobs', to='ranksearch.Property'),
        ),
        migrations.AlterUniqueTogether(
            name='property',
            unique_together=set([('name', 'owner')]),
        ),
    ]

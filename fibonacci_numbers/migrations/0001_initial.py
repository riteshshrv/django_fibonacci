# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fibonacci',
            fields=[
                ('parameter', models.IntegerField(primary_key=True, serialize=False)),
                ('result', models.CharField(max_length=200)),
            ],
        ),
    ]

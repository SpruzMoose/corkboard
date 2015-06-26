# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pintoboard',
            name='rank',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]

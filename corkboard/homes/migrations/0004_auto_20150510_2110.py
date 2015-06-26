# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homes', '0003_auto_20150510_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pin',
            name='image',
            field=models.ImageField(upload_to=b''),
            preserve_default=True,
        ),
    ]

# Generated by Django 3.2.3 on 2021-07-16 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0002_usuarioportafolio_metrica'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarioportafolio',
            name='uuid_string',
            field=models.CharField(default='none', max_length=33),
            preserve_default=False,
        ),
    ]

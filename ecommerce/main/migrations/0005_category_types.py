# Generated by Django 3.0 on 2021-04-08 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20210408_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='types',
            field=models.CharField(choices=[('1', 'Jewlery'), ('2', 'Furniture')], default='Jewlery', max_length=2),
        ),
    ]
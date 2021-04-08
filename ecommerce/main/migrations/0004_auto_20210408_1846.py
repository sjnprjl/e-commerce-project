# Generated by Django 3.0 on 2021-04-08 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_item_h_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='Brand',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ManyToManyField(to='main.Category'),
        ),
    ]
# Generated by Django 4.2.11 on 2024-04-07 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0003_bookingreviewer_visible_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingreviewer',
            name='visible_password',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='PassWord'),
        ),
    ]

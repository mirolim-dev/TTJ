# Generated by Django 4.2.11 on 2024-04-28 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ttj', '0012_stuff_ttj'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='visible_password',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='PassWord'),
        ),
    ]

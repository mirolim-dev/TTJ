# Generated by Django 4.2.11 on 2024-03-08 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ttj', '0003_admission'),
    ]

    operations = [
        migrations.AddField(
            model_name='admission',
            name='status',
            field=models.IntegerField(choices=[(0, 'Bekor qilingan'), (1, 'Active')], default=1),
        ),
    ]

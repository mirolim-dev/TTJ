# Generated by Django 4.2.11 on 2024-03-15 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ttj', '0008_alter_staff_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bed',
            name='status',
            field=models.IntegerField(blank=True, choices=[(0, 'Joy qolmagan'), (1, 'Foydalanishga berilmagan'), (2, "Bo'sh"), (3, "Bo'sh joylar bor")], null=True),
        ),
    ]

# Generated by Django 4.2.11 on 2024-05-08 05:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0004_alter_bookingreviewer_visible_password'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookingreviewer',
            options={'verbose_name_plural': "So'rovlarni ko'ruvchi shaxs"},
        ),
        migrations.AlterModelOptions(
            name='faculty',
            options={'ordering': ['name'], 'verbose_name_plural': 'Fakultetlar'},
        ),
        migrations.AlterModelOptions(
            name='university',
            options={'ordering': ['-joined_at'], 'verbose_name_plural': 'Universitet'},
        ),
        migrations.AlterField(
            model_name='bookingreviewer',
            name='is_working',
            field=models.BooleanField(default=True, verbose_name='Ishlayotganlik statusi'),
        ),
        migrations.AlterField(
            model_name='bookingreviewer',
            name='salary',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15, verbose_name='Maosh'),
        ),
        migrations.AlterField(
            model_name='bookingreviewer',
            name='university',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='university.university', verbose_name='Universitet'),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Nomi'),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='university',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='university.university', verbose_name='Universitet'),
        ),
        migrations.AlterField(
            model_name='university',
            name='joined_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name="Dasturga qo'shilgan vaqti"),
        ),
        migrations.AlterField(
            model_name='university',
            name='location',
            field=models.CharField(max_length=250, verbose_name='Manzili'),
        ),
        migrations.AlterField(
            model_name='university',
            name='location_link',
            field=models.CharField(blank=True, max_length=250, verbose_name='Mazil uchun link'),
        ),
        migrations.AlterField(
            model_name='university',
            name='name',
            field=models.CharField(max_length=250, unique=True, verbose_name='Nomi'),
        ),
    ]

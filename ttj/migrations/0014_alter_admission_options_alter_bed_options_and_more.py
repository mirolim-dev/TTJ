# Generated by Django 4.2.11 on 2024-05-08 05:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0005_alter_bookingreviewer_options_alter_faculty_options_and_more'),
        ('ttj', '0013_staff_visible_password'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='admission',
            options={'ordering': ['-created_at'], 'verbose_name_plural': 'Tayinlovlar'},
        ),
        migrations.AlterModelOptions(
            name='bed',
            options={'verbose_name': 'Yotoq', 'verbose_name_plural': 'Yotoqlar'},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={'verbose_name': 'Xona', 'verbose_name_plural': 'Xonalar'},
        ),
        migrations.AlterModelOptions(
            name='roomstuff',
            options={'verbose_name_plural': 'Xona Jihozlari'},
        ),
        migrations.AlterModelOptions(
            name='staff',
            options={'ordering': ['first_name', 'date_joined'], 'verbose_name_plural': 'Xodimlar'},
        ),
        migrations.AlterModelOptions(
            name='stuff',
            options={'verbose_name': 'Jihoz', 'verbose_name_plural': 'Jihozlar'},
        ),
        migrations.AlterModelOptions(
            name='ttj',
            options={'ordering': ['-joined_at'], 'verbose_name_plural': 'TTJ lar'},
        ),
        migrations.AlterField(
            model_name='admission',
            name='contract',
            field=models.ImageField(upload_to='ttj/contract', verbose_name='Shartnoma'),
        ),
        migrations.AlterField(
            model_name='admission',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqti'),
        ),
        migrations.AlterField(
            model_name='admission',
            name='description',
            field=models.TextField(verbose_name='Izoh'),
        ),
        migrations.AlterField(
            model_name='admission',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttj.bed', verbose_name='Xona'),
        ),
        migrations.AlterField(
            model_name='admission',
            name='status',
            field=models.IntegerField(choices=[(0, 'Bekor qilingan'), (1, 'Active')], default=1, verbose_name='Xolati'),
        ),
        migrations.AlterField(
            model_name='admission',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan vaqti"),
        ),
        migrations.AlterField(
            model_name='bed',
            name='capacity',
            field=models.IntegerField(default=4, verbose_name="Sig'imi"),
        ),
        migrations.AlterField(
            model_name='bed',
            name='status',
            field=models.IntegerField(blank=True, choices=[(0, 'Joy qolmagan'), (1, 'Foydalanishga berilmagan'), (2, "Bo'sh"), (3, "Bo'sh joylar bor")], default=2, null=True, verbose_name='Xolati'),
        ),
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Nomi'),
        ),
        migrations.AlterField(
            model_name='roomstuff',
            name='amount',
            field=models.IntegerField(verbose_name='Miqdor'),
        ),
        migrations.AlterField(
            model_name='roomstuff',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttj.room', verbose_name='Xona'),
        ),
        migrations.AlterField(
            model_name='roomstuff',
            name='stuff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttj.stuff', verbose_name='Jihoz'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='is_working',
            field=models.BooleanField(default=True, verbose_name='Ishlayabdi'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='position',
            field=models.IntegerField(choices=[(0, 'Mudir'), (1, 'Qorovul'), (2, 'Hamshira'), (3, 'Tarbiyachi'), (4, 'Farrosh')], default=2, verbose_name='Pozitisyasi'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='salary',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Maoshni UZS da kiriting', max_digits=15, verbose_name='Maosh'),
        ),
        migrations.AlterField(
            model_name='stuff',
            name='amount_of_existance',
            field=models.IntegerField(default=0, verbose_name='Mavjud miqdori'),
        ),
        migrations.AlterField(
            model_name='stuff',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Izoh'),
        ),
        migrations.AlterField(
            model_name='stuff',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Nomi'),
        ),
        migrations.AlterField(
            model_name='ttj',
            name='capacity',
            field=models.PositiveBigIntegerField(default=0, verbose_name="Sig'imi"),
        ),
        migrations.AlterField(
            model_name='ttj',
            name='joined_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name="Dasturga qo'shilgan vaqti"),
        ),
        migrations.AlterField(
            model_name='ttj',
            name='location',
            field=models.CharField(max_length=250, verbose_name='Manzili'),
        ),
        migrations.AlterField(
            model_name='ttj',
            name='location_link',
            field=models.CharField(max_length=250, verbose_name='Manzil uchun link'),
        ),
        migrations.AlterField(
            model_name='ttj',
            name='name',
            field=models.CharField(max_length=250, unique=True, verbose_name='Nomi'),
        ),
        migrations.AlterField(
            model_name='ttj',
            name='university',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='university.university', verbose_name='universitet'),
        ),
    ]

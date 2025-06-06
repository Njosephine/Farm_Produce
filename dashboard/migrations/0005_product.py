# Generated by Django 4.0.3 on 2025-04-05 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_supplier'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight_before', models.DecimalField(decimal_places=2, max_digits=10)),
                ('weight_after', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('drying_expenses', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('drying_status', models.CharField(choices=[('not_dried', 'Not Dried'), ('drying', 'Drying'), ('dried', 'Dried')], default='not_dried', max_length=50)),
                ('drying_start_date', models.DateTimeField(blank=True, null=True)),
                ('drying_end_date', models.DateTimeField(blank=True, null=True)),
                ('categoryName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.category')),
            ],
        ),
    ]

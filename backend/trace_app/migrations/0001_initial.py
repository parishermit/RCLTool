# Generated by Django 4.2.8 on 2023-12-24 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RCLLabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trace_id', models.CharField(default='', max_length=100)),
                ('operation_name', models.CharField(default='', max_length=200)),
                ('cmdb_id', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Span',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.CharField(default='', max_length=100)),
                ('cmdb_id', models.CharField(default='', max_length=100)),
                ('span_id', models.CharField(default='', max_length=100)),
                ('trace_id', models.CharField(default='', max_length=100)),
                ('duration', models.IntegerField(default=0)),
                ('type', models.CharField(default='', max_length=100)),
                ('status_code', models.CharField(default='0', max_length=100)),
                ('operation_name', models.CharField(default='', max_length=200)),
                ('parent_span', models.CharField(default='', max_length=100)),
            ],
        ),
    ]

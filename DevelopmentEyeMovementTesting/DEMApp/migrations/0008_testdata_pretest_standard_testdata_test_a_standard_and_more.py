# Generated by Django 4.2.16 on 2025-04-18 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DEMApp', '0007_testdata_test_c_additions'),
    ]

    operations = [
        migrations.AddField(
            model_name='testdata',
            name='pretest_standard',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='testdata',
            name='test_a_standard',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='testdata',
            name='test_b_standard',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='testdata',
            name='test_c_standard',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]

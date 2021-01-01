# Generated by Django 3.1.1 on 2020-12-31 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pool', '0002_auto_20201108_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='pooltarget',
            name='level',
            field=models.CharField(default='ADVANCED', max_length=12),
        ),
        migrations.AddField(
            model_name='submission',
            name='level',
            field=models.CharField(choices=[('BEGINNER', 'Beginner'), ('INTERMEDIATE', ' Intermediate'), ('ADVANCED', 'Advanced')], default='ADVANCED', max_length=12),
        ),
        migrations.AddField(
            model_name='target',
            name='level',
            field=models.CharField(default='ADVANCED', max_length=12),
        ),
        migrations.AlterField(
            model_name='pooltarget',
            name='category',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='category',
            field=models.CharField(blank=True, choices=[('PERSON', 'Person'), ('LIFEFORM', 'Lifeform'), ('OBJECT', 'Object'), ('LOCATION', 'Location'), ('EVENT', 'Event'), ('OTHER', 'Other')], max_length=12, null=True),
        ),
    ]

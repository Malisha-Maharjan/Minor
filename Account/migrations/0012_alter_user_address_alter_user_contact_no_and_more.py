# Generated by Django 4.1.3 on 2023-01-29 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0011_marks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='contact_no',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.TextField(null=True),
        ),
    ]

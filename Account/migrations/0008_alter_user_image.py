# Generated by Django 4.1.3 on 2023-01-27 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0007_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.TextField(),
        ),
    ]

# Generated by Django 4.0.1 on 2022-03-07 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='shared_to',
            field=models.ManyToManyField(related_name='shared_posts', to='blog.Blog'),
        ),
    ]

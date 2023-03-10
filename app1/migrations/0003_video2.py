# Generated by Django 3.2.7 on 2023-03-03 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_alter_video_caption'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.DateField(default='NA')),
                ('video', models.FileField(upload_to='video')),
                ('processed_video', models.FileField(default='Na', upload_to='processed_video')),
            ],
        ),
    ]

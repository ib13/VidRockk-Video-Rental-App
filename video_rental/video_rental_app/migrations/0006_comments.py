# Generated by Django 2.1.1 on 2018-09-14 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('video_rental_app', '0005_auto_20180913_1242'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=20)),
                ('comment', models.TextField(max_length=200)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='video_rental_app.Video')),
            ],
        ),
    ]

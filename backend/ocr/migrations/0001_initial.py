# Generated by Django 2.0.6 on 2018-07-08 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OCR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_path', models.ImageField(default='img/default.jpg', upload_to='img/')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('pred_char', models.CharField(max_length=1)),
            ],
        ),
    ]

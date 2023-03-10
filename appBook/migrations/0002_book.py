# Generated by Django 2.2.4 on 2022-12-27 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appBook', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('desc', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('faverite_book', models.ManyToManyField(default='', related_name='faverite_books', to='appBook.User')),
                ('upload_book', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='upload_books', to='appBook.User')),
            ],
        ),
    ]

# Generated by Django 3.0.4 on 2020-04-19 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0005_playlist_date_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RenameField(
            model_name='album',
            old_name='artist_id',
            new_name='artist',
        ),
        migrations.RenameField(
            model_name='playlist',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='song',
            old_name='album_id',
            new_name='album',
        ),
        migrations.RenameField(
            model_name='song',
            old_name='artist_id',
            new_name='artist',
        ),
        migrations.AddField(
            model_name='playlist',
            name='genres',
            field=models.ManyToManyField(to='playlists.Genre'),
        ),
    ]
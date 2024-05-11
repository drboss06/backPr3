# Generated by Django 5.0.2 on 2024-05-10 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0014_rename_post_comment_post_commented'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='post_commented',
        ),
        migrations.AddField(
            model_name='post',
            name='comment',
            field=models.ManyToManyField(blank=True, to='blogs.comment'),
        ),
    ]

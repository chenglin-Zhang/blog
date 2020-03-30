# Generated by Django 2.0 on 2020-03-30 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=50, verbose_name='昵称')),
                ('content', models.TextField(verbose_name='内容')),
                ('icon', models.CharField(default='images/tx1.jpg', max_length=150, verbose_name='头像')),
                ('date', models.DateField(auto_now_add=True, verbose_name='留言时间')),
            ],
            options={
                'verbose_name': '留言表',
                'verbose_name_plural': '留言表',
                'db_table': 'message',
            },
        ),
    ]

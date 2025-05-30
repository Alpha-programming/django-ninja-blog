# Generated by Django 5.1.6 on 2025-02-18 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0002_rename_faq_slider'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(verbose_name='Вопрос')),
                ('answer', models.TextField(verbose_name='Ответ')),
            ],
            options={
                'verbose_name': 'Вопросы ответы',
            },
        ),
        migrations.AlterModelOptions(
            name='slider',
            options={'verbose_name': 'Слайд', 'verbose_name_plural': 'Слайды'},
        ),
        migrations.AlterField(
            model_name='slider',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='slider',
            name='image',
            field=models.ImageField(upload_to='slider/', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='slider',
            name='title',
            field=models.CharField(max_length=40, verbose_name='Заголовок'),
        ),
    ]

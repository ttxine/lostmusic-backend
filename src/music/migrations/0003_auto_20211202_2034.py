# Generated by Django 3.2.9 on 2021-12-02 17:34

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django_resized.forms
import src.base.services


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0002_favorites'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='cover',
            field=models.ImageField(default='image.png', upload_to=src.base.services.get_cover_upload_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png']), src.base.services.validate_file_size], verbose_name='Обложка'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='album',
            name='cover_large',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format='JPEG', keep_meta=True, quality=90, size=[250, 250], upload_to=src.base.services.get_cover_upload_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png']), src.base.services.validate_file_size], verbose_name='Обложка большая'),
        ),
        migrations.AlterField(
            model_name='album',
            name='cover_small',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format='JPEG', keep_meta=True, quality=90, size=[100, 100], upload_to=src.base.services.get_cover_upload_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png']), src.base.services.validate_file_size], verbose_name='Обложка малая'),
        ),
        migrations.AlterField(
            model_name='album',
            name='featuring',
            field=models.ManyToManyField(blank=True, related_name='albums_featuring', to=settings.AUTH_USER_MODEL, verbose_name='С участием'),
        ),
        migrations.AlterField(
            model_name='track',
            name='featuring',
            field=models.ManyToManyField(blank=True, related_name='tracks_featuring', to=settings.AUTH_USER_MODEL, verbose_name='С участием'),
        ),
    ]

from django.contrib import admin

from src.music import models

admin.site.register(models.Album)
admin.site.register(models.Track)
admin.site.register(models.Genre)

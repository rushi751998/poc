from django.contrib import admin
# Register your models here.
from .models import Video,person_db
admin.site.register(Video)
admin.site.register(person_db)
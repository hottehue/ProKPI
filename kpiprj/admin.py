from django.contrib import admin

# Register your models here.

from .models import Project, TempLoad, Phase
admin.site.register(Project)
admin.site.register(TempLoad)
admin.site.register(Phase)
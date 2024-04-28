from django.contrib import admin

# Register your models here.

from .models import Project, TempLoad, Phase, Phase_ref
admin.site.register(Project)
admin.site.register(TempLoad)
admin.site.register(Phase)
admin.site.register(Phase_ref)
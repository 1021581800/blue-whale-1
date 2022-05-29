from django.contrib import admin

# Register your models here.
from saasapp.sops_task.models import Tasks

admin.site.register(Tasks)

from django.contrib import admin

# Register your models here.
from .models import Paper
from .models import Mapping


admin.site.register(Paper)
admin.site.register(Mapping)
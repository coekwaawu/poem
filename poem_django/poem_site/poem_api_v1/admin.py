from django.contrib import admin
from .models import Poem_V1, PoemTag, PoemTagRelationship
# Register your models here.

admin.site.register(Poem_V1)
admin.site.register(PoemTag)
admin.site.register(PoemTagRelationship)

from django.contrib import admin
from .models import Poem, PoemTag, PoemTagRelationship
# Register your models here.

admin.site.register(Poem)
admin.site.register(PoemTag)
admin.site.register(PoemTagRelationship)

from django.contrib import admin
from .models import Poem, Tag, PoemTag
# Register your models here.

admin.site.register(Poem)
admin.site.register(Tag)
admin.site.register(PoemTag)

from django.contrib import admin
from .models import Poem, PoemTag, PoemTagRelationship, PoemContent, PoemYi, PoemZhu, PoemShang, PoemAuthor
# Register your models here.

admin.site.register(Poem)
admin.site.register(PoemTag)
admin.site.register(PoemContent)
admin.site.register(PoemTagRelationship)
admin.site.register(PoemYi)
admin.site.register(PoemZhu)
admin.site.register(PoemShang)
admin.site.register(PoemAuthor)


from django.db import models

# Create your models here.


class PoemTag(models.Model):
    poem_tag_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'poem_tag'

    def __str__(self):
        return self.name


class PoemAuthor(models.Model):
    poem_author_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=10)


class Poem(models.Model):
    poem_id = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=50, blank=True, null=True)
    dynasty = models.CharField(max_length=20, blank=True, null=True)
    author = models.ForeignKey(PoemAuthor, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    poemtags = models.ManyToManyField(PoemTag, through='PoemTagRelationship')
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'poem'

    def __str__(self):
        return self.title


class PoemTagRelationship(models.Model):
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE)
    poem_tag = models.ForeignKey(PoemTag, on_delete=models.CASCADE)

    class Meta:
        db_table = "poem_tag_relationship"

    def __str__(self):
        return self.poem.title+'-'+self.poem_tag.name

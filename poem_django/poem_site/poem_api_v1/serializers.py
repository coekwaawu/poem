from rest_framework import serializers
from .models import Poem_V1, PoemTag, PoemTagRelationship
from django.contrib.auth.models import User

class PoemTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = PoemTag
        fields = '__all__'


class PoemSerializer(serializers.ModelSerializer):

    poemtags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Poem_V1
        fields = ('url', 'poem_id', 'title', 'dynasty', 'author', 'content', 'yi', 'zhu',
                  'shang', 'yizhu', 'yishang', 'zhushang', 'yizhushang', 'poemtags', 'owner')


class PoemTagRelationshipSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PoemTagRelationship
        fields = ('id', 'poem_id', 'poem_tag_id')


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'poems')




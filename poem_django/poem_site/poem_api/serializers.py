from rest_framework import serializers
from poem_api.models import Poem, PoemTag, PoemTagRelationship
from django.contrib.auth.models import User


class PoemTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = PoemTag
        fields = '__all__'


class PoemSerializer(serializers.ModelSerializer):

    poemtags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Poem
        fields = ('url', 'poem_id', 'title', 'dynasty', 'author', 'content', 'yi', 'zhu',
                  'shang', 'yizhu', 'yishang', 'zhushang', 'yizhushang', 'poemtags', 'owner')


class PoemTagRelationshipSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PoemTagRelationship
        fields = ('id', 'poem_id', 'poem_tag_id')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    #poems = serializers.HyperlinkedRelatedField(many=True, view_name='poem-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'poems')




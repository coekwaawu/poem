from rest_framework import serializers
from poem_api.models import Poem, PoemTag, Tag
from django.contrib.auth.models import User


class PoemSerializer(serializers.ModelSerializer):

    poemtag_set = serializers.StringRelatedField(many=True)

    class Meta:
        model = Poem
        fields = ('url', 'poem_id', 'title', 'dynasty', 'author', 'content', 'yi', 'zhu',
                  'shang', 'yizhu', 'yishang', 'zhushang', 'yizhushang', 'poemtag_set', 'owner')


class PoemTagSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PoemTag
        fields = ('id', 'poem_id', 'tag_id')


class TagSerializer(serializers.ModelSerializer):

    poems = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='poem-detail')

    class Meta:
        model = Tag
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    #poems = serializers.HyperlinkedRelatedField(many=True, view_name='poem-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'poems')




from rest_framework import serializers
from .models import Poem, PoemTag, PoemTagRelationship, PoemContent, PoemYi, PoemZhu, PoemShang, PoemAuthor
from django.contrib.auth.models import User

class PoemTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = PoemTag
        fields = '__all__'


class PoemSerializer(serializers.ModelSerializer):

    poemtags = serializers.StringRelatedField(many=True)
    content = serializers.StringRelatedField(many=True)
    yi = serializers.StringRelatedField(many=True)
    zhu = serializers.StringRelatedField(many=True)
    shang = serializers.StringRelatedField(many=True)

    class Meta:
        model = Poem
        fields = ('url', 'poem_id', 'title', 'dynasty', 'author', 'content', 'yi', 'zhu',
                  'shang', 'poemtags')


class PoemTagRelationshipSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PoemTagRelationship
        fields = ('id', 'poem_id', 'poem_tag_id')


class PoemAuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = PoemAuthor
        fields = ('poem_author_id', 'name')


class PoemContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PoemContent
        fields = ('poem_content_id', 'poem_id', 'content', 'order_number')


class PoemYiSerializer(serializers.ModelSerializer):

    class Meta:
        model = PoemYi
        fields = ('poem_yi_id', 'poem_id', 'yi', 'poem_content_id')


class PoemZhuSerializer(serializers.ModelSerializer):

    class Meta:
        model = PoemZhu
        fields = ('poem_zhu_id', 'poem_id', 'zhu', 'poem_content_id')


class PoemShangSerializer(serializers.ModelSerializer):

    class Meta:
        model = PoemShang
        fields = ('poem_shang_id', 'poem_id', 'shang', 'poem_content_id')


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'poems')




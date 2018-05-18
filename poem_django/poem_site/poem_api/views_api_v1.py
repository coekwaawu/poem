from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.reverse import reverse
from rest_framework import permissions
from rest_framework import viewsets
from poem_api.permissions import IsOwnerOrReadOnly
from poem_api.models import Poem
from poem_api.models import Tag
from poem_api.serializers import PoemSerializer
from poem_api.serializers import UserSerializer
from poem_api.serializers import TagSerializer


class PoemViewSet(viewsets.ModelViewSet):
    queryset = Poem.objects.all()
    serializer_class = PoemSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('title', 'author', 'content')
    ordering_fields = ('title', 'author', 'dynasty')

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def content(self, request, *args, **kwargs):
        poem = self.get_object()
        return Response(poem.content)

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def author(self, request, *args, **kwargs):
        poem = self.get_object()
        return Response(poem.author)

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def poemtag(self, request, *args, **kwargs):
        poem = self.get_object()
        return Response(poem.poemtag_set.all())

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.annotate(number_of_poems=Count('poems'))
    serializer_class = TagSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('name', )
    ordering_fields = ('number_of_poems', 'name', )

    '''
    def get_queryset(self):
        queryset = Tag.objects.annotate(Count('poems'))
        return queryset.order_by()
    '''

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'poems': reverse('poem-list', request=request, format=format),
        'tags': reverse('tag-list', request=request, format=format),
    })


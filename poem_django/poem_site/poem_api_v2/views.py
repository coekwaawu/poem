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
from rest_framework import viewsets
from .models import Poem
from .models import PoemTag
from .serializers import PoemSerializer
from .serializers import UserSerializer
from .serializers import PoemTagSerializer


class PoemViewSet(viewsets.ModelViewSet):
    queryset = Poem.objects.all()
    serializer_class = PoemSerializer
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


class PoemTagViewSet(viewsets.ModelViewSet):
    queryset = PoemTag.objects.all().annotate(number_of_poems=Count('poem'))
    serializer_class = PoemTagSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('name', )
    ordering_fields = ('number_of_poems', 'name', )


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'poems': reverse('poem-list', request=request, format=format),
        'poemtags': reverse('poemtag-list', request=request, format=format),
    })
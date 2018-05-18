from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import renderers
from . import views_api_v1
from poem_api.views_api_v1 import PoemViewSet, UserViewSet, api_root


poem_list = PoemViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
poem_detail = PoemViewSet.as_view({
    'get': 'retreive',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
poem_content = PoemViewSet.as_view({
    'get': 'content'
}, renderer_classes=[renderers.StaticHTMLRenderer])
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})


urlpatterns = [
	path('', api_root),
	path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	path('poems/', poem_list, name='poem-list'),
	path('poems/<str:pk>/', poem_detail, name='poem-detail'),
    path('poems/<str:pk>/content/', poem_content, name='poem-content'),
    path('user/', user_list, name='user-list'),
    path('user/<str:pk>/', user_detail, name='user-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
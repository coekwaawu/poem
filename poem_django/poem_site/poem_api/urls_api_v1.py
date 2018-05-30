from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from . import views_api_v1


router = DefaultRouter()
router.register('poems', views_api_v1.PoemViewSet)
router.register('users', views_api_v1.UserViewSet)
router.register('poemtags', views_api_v1.PoemTagViewSet)
schema_view = get_schema_view(title='Pastebin API')


urlpatterns = [
    path('', include(router.urls)),
    path('schema/', schema_view)
]

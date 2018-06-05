from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('poems', views.PoemViewSet)
router.register('users', views.UserViewSet)
router.register('poemtags', views.PoemTagViewSet)


urlpatterns = [
    path('', include(router.urls)),
]

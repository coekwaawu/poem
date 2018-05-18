from django.urls import path
from . import views

urlpatterns = [
	path('', views.test,name="test"),
	path('<str:poem_title>/poem_id/', views.poem_id,name="poem_id"),
	path('<str:poem_id>/title/', views.title,name="title"),
	path('<str:poem_id>/dynasty/', views.dynasty,name="dynasty"),
	path('<str:poem_id>/author/', views.author,name="author"),
	path('<str:poem_id>/content/', views.content,name="content"),
	path('<str:poem_id>/yi/', views.yi,name="yi"),
	path('<str:poem_id>/zhu/', views.zhu,name="zhu"),
	path('<str:poem_id>/shang/', views.shang,name="shang"),
	path('<str:poem_id>/', views.poem,name="poem"),
]
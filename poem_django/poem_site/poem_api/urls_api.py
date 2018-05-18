from django.urls import path
from . import views

urlpatterns = [
	path('<int:curPage>', views.api, name="api"),
]
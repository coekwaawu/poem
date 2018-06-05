from django.urls import path
from NoRESTfulFramework import views

urlpatterns = [
	path('<int:curPage>', views.api, name="api"),
]
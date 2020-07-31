from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("",UserListView.as_view(),name="userList"),
    path("new/",CreateUserView.as_view(),name="create_user"),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
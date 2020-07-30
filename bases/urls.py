from django.urls import path,include
from django.contrib.auth import views as auth_views
from bases.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("",LoginFormView.as_view(),name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("home/",DashBoardView.as_view(),name="casa"),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
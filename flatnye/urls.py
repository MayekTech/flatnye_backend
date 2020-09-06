"""flatnye URL Configuration"""

from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.urls import path, include
from rest_framework.authtoken import views as tokenViews
from rest_framework.routers import DefaultRouter
from .api import views


# Un router qui va patcher mes viewsets.
router = DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'compte', views.CompteViewSet)
router.register(r'bien', views.BienSet)
router.register(r'bien/media', views.MediaSet)
router.register(r'visite', views.VisiteSet)
router.register(r'notation', views.NotationSet)
router.register(r'commentaire', views.CommentSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth', include('rest_framework.urls')),
    path('api/get_token/', tokenViews.obtain_auth_token),

]

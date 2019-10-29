from django.conf.urls import include
from django.urls import path
from rest_framework import renderers
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from api import views

router = DefaultRouter()
router.register(r'game', views.GameViewSet)
router.register(r'version', views.VersionViewSet)
router.register(r'edition', views.EditionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls')),
]
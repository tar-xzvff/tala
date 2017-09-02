from django.conf.urls import url, include
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r'nodes', views.NodeViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]

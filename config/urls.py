"""
URL configuration for chat_bot_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.chat.api.viewsets import ChatRoomViewSet, ChatMessageViewSet, FileViewSet, HeartbeatViewSet

router = DefaultRouter()
router.register("chat/rooms", ChatRoomViewSet, basename="chat-rooms")
router.register("chat/messages", ChatMessageViewSet, basename="chat-messages")
router.register("chat/files", FileViewSet, basename="chat-files")
router.register("health", HeartbeatViewSet, basename="health")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/authentication/', include('dj_rest_auth.urls')),
    path('api/authentication/registration/', include('dj_rest_auth.registration.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
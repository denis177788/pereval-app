from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from main import views
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect


router = routers.DefaultRouter()
router.register(r'submitData', views.PerevalViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]


# включаем возможность обработки картинок
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

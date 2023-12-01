from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from main import views
from django.conf.urls.static import static
from django.conf import settings


router = routers.DefaultRouter()
router.register(r'users', views.UserViewset)
router.register(r'coords', views.CoordsViewset)
router.register(r'level', views.LevelViewset)
router.register(r'images', views.ImagesViewest)
router.register(r'pereval', views.PerevalViewest)


urlpatterns = [
   path('admin/', admin.site.urls),
   path('', include(router.urls)),
   path('api/submitData/', include(router.urls)),
   path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]


# включаем возможность обработки картинок
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

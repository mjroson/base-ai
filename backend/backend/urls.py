from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from apps.image_net.api import PredictApiView, OcrTrackModelViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'ocr', OcrTrackModelViewSet)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('predict/', PredictApiView.as_view()),
                  path('api/', include(router.urls)),
              ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

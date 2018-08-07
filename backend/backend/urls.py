from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from image_net.api import PredictApiView


urlpatterns = [
                  path('admin/', admin.site.urls),
                  #path('ocr/', include('ocr.urls')),
                  path('predict/', PredictApiView.as_view()),
              ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

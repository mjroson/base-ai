from django.conf.urls import url
from .views import (
    OCRListView,
    OCRDetailView,
    OCRCreateView,
    OCRDeleteView,
    OCRUpdateView,
)

urlpatterns = [
    url(r'^$', OCRListView.as_view()),
    url(r'^(?P<pk>\d+)/$', OCRDetailView.as_view()),
    url(r'^create/$', OCRCreateView.as_view()),
    url(r'^update/(?P<pk>\d+)/$', OCRUpdateView.as_view()),
    url(r'^delete/(?P<pk>\d+)/$', OCRDeleteView.as_view()),
]

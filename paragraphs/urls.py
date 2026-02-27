from django.urls import path

from .views import ParagraphIngestView, ParagraphSearchView

urlpatterns = [
    path('ingest/', ParagraphIngestView.as_view(), name='paragraph-ingest'),
    path('search/', ParagraphSearchView.as_view(), name='paragraph-search'),
]

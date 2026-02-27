from django.contrib import admin

from .models import Paragraph, ParagraphWordCount, WordFrequency

admin.site.register(Paragraph)
admin.site.register(ParagraphWordCount)
admin.site.register(WordFrequency)

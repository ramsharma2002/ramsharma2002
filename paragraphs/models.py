from django.conf import settings
from django.db import models


class Paragraph(models.Model):
    """Paragraph entry linked to a user."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='paragraphs')
    content = models.TextField()
    sequence = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'sequence')
        ordering = ['sequence']


class WordFrequency(models.Model):
    """Word occurrence count per user across all paragraphs."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='word_frequencies')
    word = models.CharField(max_length=255)
    frequency = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'word')
        ordering = ['-frequency', 'word']


class ParagraphWordCount(models.Model):
    """Word count for each paragraph used for ranking search results."""

    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE, related_name='word_counts')
    word = models.CharField(max_length=255)
    count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('paragraph', 'word')
        ordering = ['-count']

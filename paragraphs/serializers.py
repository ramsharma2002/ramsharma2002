from rest_framework import serializers

from .models import Paragraph


class ParagraphBulkInputSerializer(serializers.Serializer):
    """Serializer for accepting multiple paragraphs in one request."""

    text = serializers.CharField(help_text='Multiple paragraphs separated by two newline characters.')


class ParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paragraph
        fields = ['id', 'sequence', 'content', 'created_date']


class ParagraphSearchResultSerializer(serializers.Serializer):
    paragraph_id = serializers.IntegerField()
    sequence = serializers.IntegerField()
    occurrences = serializers.IntegerField()
    content = serializers.CharField()

from django.db import transaction
from django.db.models import F
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Paragraph, ParagraphWordCount, WordFrequency
from .serializers import ParagraphBulkInputSerializer, ParagraphSearchResultSerializer
from .tasks import recalculate_user_word_frequencies
from .utils import normalize_tokens


class ParagraphIngestView(APIView):
    """Accept bulk paragraph text and store token frequencies."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ParagraphBulkInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        raw_paragraphs = [p.strip() for p in serializer.validated_data['text'].split('\n\n') if p.strip()]
        if not raw_paragraphs:
            return Response({'detail': 'No paragraphs found in payload.'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        created_ids = []
        base_sequence = (user.paragraphs.order_by('-sequence').values_list('sequence', flat=True).first() or 0) + 1

        with transaction.atomic():
            for index, content in enumerate(raw_paragraphs, start=base_sequence):
                paragraph = Paragraph.objects.create(user=user, content=content, sequence=index)
                token_counts = normalize_tokens(content)

                ParagraphWordCount.objects.bulk_create(
                    [
                        ParagraphWordCount(paragraph=paragraph, word=word, count=count)
                        for word, count in token_counts.items()
                    ]
                )

                for word, count in token_counts.items():
                    freq_obj, _ = WordFrequency.objects.get_or_create(user=user, word=word, defaults={'frequency': 0})
                    freq_obj.frequency = F('frequency') + count
                    freq_obj.save(update_fields=['frequency'])

                created_ids.append(paragraph.id)

        recalculate_user_word_frequencies.delay(user.id)

        return Response(
            {'created_paragraph_ids': created_ids, 'count': len(created_ids)},
            status=status.HTTP_201_CREATED,
        )


class ParagraphSearchView(generics.GenericAPIView):
    """Search a word and return top 10 paragraphs with max occurrences for current user."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ParagraphSearchResultSerializer

    def get(self, request):
        word = request.query_params.get('word', '').strip().lower()
        if not word:
            return Response({'detail': 'Query parameter "word" is required.'}, status=status.HTTP_400_BAD_REQUEST)

        counts = (
            ParagraphWordCount.objects
            .filter(paragraph__user=request.user, word=word)
            .select_related('paragraph')
            .order_by('-count', 'paragraph__sequence')[:10]
        )

        results = [
            {
                'paragraph_id': item.paragraph.id,
                'sequence': item.paragraph.sequence,
                'occurrences': item.count,
                'content': item.paragraph.content,
            }
            for item in counts
        ]

        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)

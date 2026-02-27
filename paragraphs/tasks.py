from celery import shared_task
from django.contrib.auth import get_user_model
from django.db.models import Sum

from .models import WordFrequency


@shared_task

def recalculate_user_word_frequencies(user_id: int):
    """Recalculate user-level word frequency based on paragraph-level counts."""

    user_model = get_user_model()
    user = user_model.objects.filter(id=user_id).first()
    if not user:
        return {'status': 'skipped', 'reason': 'user_not_found'}

    aggregated = (
        user.paragraphs.values('word_counts__word')
        .annotate(total=Sum('word_counts__count'))
        .exclude(word_counts__word__isnull=True)
    )

    WordFrequency.objects.filter(user=user).delete()
    WordFrequency.objects.bulk_create(
        [
            WordFrequency(user=user, word=item['word_counts__word'], frequency=item['total'])
            for item in aggregated
        ]
    )

    return {'status': 'ok', 'words': len(aggregated)}


@shared_task
def recalculate_all_users_word_frequencies():
    """Scheduled task to recalculate frequencies for all users."""

    user_model = get_user_model()
    total = 0
    for user in user_model.objects.all().iterator():
        recalculate_user_word_frequencies(user.id)
        total += 1
    return {'status': 'ok', 'users_processed': total}

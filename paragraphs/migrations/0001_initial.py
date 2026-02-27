# Generated manually for offline environment
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Paragraph',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('sequence', models.PositiveIntegerField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paragraphs', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['sequence'], 'unique_together': {('user', 'sequence')}},
        ),
        migrations.CreateModel(
            name='WordFrequency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=255)),
                ('frequency', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='word_frequencies', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-frequency', 'word'], 'unique_together': {('user', 'word')}},
        ),
        migrations.CreateModel(
            name='ParagraphWordCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=255)),
                ('count', models.PositiveIntegerField(default=0)),
                ('paragraph', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='word_counts', to='paragraphs.paragraph')),
            ],
            options={'ordering': ['-count'], 'unique_together': {('paragraph', 'word')}},
        ),
    ]

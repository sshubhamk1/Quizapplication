# quiz / models.py

from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from taggit.managers import TaggableManager
from modelcluster.models import ClusterableModel
from wagtail.snippets.models import register_snippet


# Snippet: Subject
@register_snippet
class Subject(models.Model):
    name = models.CharField(max_length=100)

    panels = [FieldPanel("name")]

    def __str__(self):
        return self.name


class QuestionTag(TaggedItemBase):
    content_object = ParentalKey(
        "QuestionPage", related_name="tagged_items", on_delete=models.CASCADE
    )


DIFFICULTY_CHOICES = [
    ("easy", "Easy"),
    ("medium", "Medium"),
    ("hard", "Hard"),
]


class QuestionPage(Page):
    question_text = RichTextField()
    subject = models.ForeignKey(
        "quiz.Subject",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="questions",
    )
    difficulty = models.CharField(
        max_length=10, choices=DIFFICULTY_CHOICES, default="medium"
    )
    tags = TaggableManager(through=QuestionTag, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("question_text"),
        PageChooserPanel("subject"),
        FieldPanel("difficulty"),
        FieldPanel("tags"),
        InlinePanel("options", label="Options"),
    ]


class Option(models.Model):
    question = ParentalKey(
        "QuestionPage", related_name="options", on_delete=models.CASCADE
    )
    text = RichTextField()
    is_correct = models.BooleanField(default=False)

    panels = [FieldPanel("text"), FieldPanel("is_correct")]


from django.db import models

from taggit.managers import TaggableManager

from polymorphic import PolymorphicModel


class Fragment(PolymorphicModel):
    description = models.CharField(max_length=200, blank=True)
    tags = TaggableManager(blank=True)

    template_names = ['bob/fragment/default.html']

    def render(self):
        raise NotImplementedError


class TextFragment(Fragment):
    content = models.TextField(blank=True)

    template_names = ['bob/fragment/text.html']

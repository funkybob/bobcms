
from django.db import models
from django import template
from django.utils.functional import cached_property

from polymorphic import PolymorphicModel


class Tracking(models.Model):
    '''
    ABC for keeping created/edited fields up to date.
    '''
    created = models.DateTimeField(default=timezone.now, editable=False)
    edited = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.edited = timezone.now()
        return super().save(*args, **kwargs)


class Page(Tracking):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    @cached_property
    def fragment(self):
        return {
            f.name: f
            for f in self.fragments.all()
        }


class PageProcessor(Tracking):
    page = models.ForignKey('Page', related_name='processors')
    order = models.IntegerField(default=0)
    processor = models.ForeignKey('processors.Processor')

    class Meta:
        ordering = ('order',)


class Processor(Tracking, PolymorphicModel):
    '''
    Base class for a Page processor.
    '''
    description = models.CharField(max_length=200, blank=True)


class Template(Tracking):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)

    @cached_property
    def tmpl(self):
        return template.Template(self.content)

    def render(self, context):
        return self.tmpl.render(context)


class PageFragment(Tracking):
    '''
    Binds a fragment to a slot on a Page.
    '''
    page = models.ForeignKey('Page', related_name='fragments')
    name = models.SlugField()
    fragment = models.ForeignKey('fragments.Fragment')

    class Meta:
        unique_together = ('page', 'name',)


class Fragment(Tracking, PolymorphicModel):
    description = models.CharField(max_length=200, blank=True)
    tags = TaggableManager(blank=True)

    template_names = ['bob/fragment/default.html']

    def render(self):
        raise NotImplementedError


class TextFragment(Fragment):
    content = models.TextField(blank=True)

    template_names = ['bob/fragment/text.html']


from django.db import models
from django import template
from django.utils.functional import cached_property


class Page(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    @cached_property
    def fragment(self):
        return {
            f.name: f
            for f in self.fragments.all()
        }


class PageProcessor(models.Model):
    page = models.ForignKey('Page', related_name='processors')
    order = models.IntegerField(default=0)
    processor = models.ForeignKey('processors.Processor')

    class Meta:
        ordering = ('order',)


class PageFragment(models.Model):
    page = models.ForeignKey('Page', related_name='fragments')
    name = models.SlugField()
    fragment = models.ForeignKey('fragments.Fragment')

    class Meta:
        unique_together = ('page', 'name',)


class Template(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)

    @cached_property
    def tmpl(self):
        return template.Template(self.content)

    def render(self, context):
        return self.tmpl.render(context)

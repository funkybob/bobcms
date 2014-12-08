
from django import template
from django.template.loaders import select_template

register = template.Library()


class PlaceholderNode(template.Node):
    def __init__(self, name, **kwargs):
        self.name = name
        self.kwargs = kwargs

    def render(self, context):
        name = self.name.resolve(context)
        kwargs = {
            name: value.resolve(context)
            for name, value in self.kwargs.items()
        }
        kwargs['fragment'] = fragment = context['page'].fragment[name]

        template_names = fragment.template_names[:]
        if 'template' in kwargs:
            template_names.insert(0, kwargs.pop('template'))

        tmpl = select_template(template_names)

        with context.push(**kwargs):
            return tmpl.render(context)


@register.tag
def placeholder(parser, token):
    bits = token.contents.split()

    try:
        name = bits.pop(0)
    except IndexError:
        raise template.TemplateSyntaxError(
            'Placeholder requires one positional argument'
        )
    try:
        name = template.Variable(name).resolve({})
    except template.VariableDoesNotExist:
        raise template.TemplateSyntaxError(
            'Placeholder name must be a literal.'
        )

    kwargs = template.token_kwargs(bits, parser)

    if bits:
        raise template.TemplateSyntaxError(
            'Placeholder accepts only one positional argument.'
        )

    return PlaceholderNode(name, **kwargs)

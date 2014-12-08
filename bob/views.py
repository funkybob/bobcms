
from django.views import generic

from .models import Page
from .processors.models import Processor


class PageView(generic.TemplateView):

    def apply_processors(self, action, *args, **kwargs):
        def dummy(*args, **kwargs):
            return None

        for processor in self.processors:
            result = getattr(processor, action, dummy)(self, *args, **kwargs)
            if result is not None:
                return result
        return None

    def dispatch(self, request, path, *args, **kwargs):
        self.page = page = Page.objects.get(pagemap__path=path)
        self.processors = list(
            Processor.objects
                     .filter(pageprocessor__page=page)
                     .order_by('pageprocessor__order')
        )

        result = self.apply_processors('dispatch')
        if result is not None:
            return result

        method = request.method.lower()
        if method in self.http_method_names:
            handler = getattr(self, method, self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed

        result = self.apply_processors(method, *args, **kwargs)
        if result is None:
            result = handler(request, *args, **kwargs)

        return result

    def get_context_data(self, **kwargs):
        kwargs['page'] = self.page

        for processor in self.processors:
            if hasattr(processor, 'get_context_data'):
                kwargs = processor.get_context_data(**kwargs)
        return super().get_context_data(**kwargs)

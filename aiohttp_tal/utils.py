import chameleon

from .exceptions import TemplateNotFound


def app_function_wrapper(app, f):
    def f_wrapped(*args, **kwargs):
        return f(app, *args, **kwargs)
    return f_wrapped


class Environment():

    def __init__(self, loader):
        self.globals = {}
        self.filters = {}
        self._loader = loader

    def get_template(self, template_name):
        try:
            template = self._loader[template_name]
        except KeyError:
            raise TemplateNotFound(template_name)
        if isinstance(template, str):
            template = chameleon.PageTemplate(template)
        return template

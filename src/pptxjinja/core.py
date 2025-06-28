from jinja2 import Environment, FileSystemLoader

from .jinja_ext.splitslide import SplitSlideExtension
from .render_engine import build_rendered_presentation

class Template:
    def __init__(self, template_path):
        self.template_path = template_path
        self.presentation = None
        self.env = Environment(loader=FileSystemLoader("."))  # of correcte pad

    def render(self, context):
        # Zet context en split config in globals voor de extension
        self.env.add_extension(SplitSlideExtension)
        self.env.globals['context'] = context
        self.env.globals['split_config'] = context.get('split', {})

        self.presentation = build_rendered_presentation(self.template_path, context, env=self.env)
        return self

    def save(self, path):
        if self.presentation:
            self.presentation.save(path)
        else:
            raise RuntimeError("No presentation rendered yet. Call render() first.")

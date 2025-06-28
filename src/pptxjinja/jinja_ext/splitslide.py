from jinja2 import nodes
from jinja2.ext import Extension
from jinja2.runtime import Undefined
from jinja2 import pass_context

class SplitSlideExtension(Extension):
    tags = {"splitslide"}

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        target = parser.parse_assign_target()
        var_name = target.name if isinstance(target, nodes.Name) else str(target)

        parser.stream.expect('name:in')
        collection = parser.parse_expression()

        body = parser.parse_statements(['name:endsplitslide'], drop_needle=True)

        return nodes.CallBlock(
            self.call_method('_render_splitslide', [nodes.Const(var_name), collection]),
            [], [nodes.Name(var_name, 'param')],
            body
        ).set_lineno(lineno)

    @pass_context
    def _render_splitslide(self, context, var_name, collection_name, caller):
        global_context = self.environment.globals.get("context", {})
        split_config = self.environment.globals.get("split_config", {})

        rows = global_context.get("collections", {}).get(collection_name, {}).get("rows", [])
        conf = split_config.get(collection_name, {})
        max_per_slide = conf.get("max_per_slide", 1)

        output = []
        chunks = [rows[i:i + max_per_slide] for i in range(0, len(rows), max_per_slide)]
        for chunk in chunks:
            print(f"🔹 Rendering chunk: {chunk}")
            try:
                rendered = context.call(caller, **{var_name: chunk})
                print(f"🔸 Rendered: {rendered}")
                output.append(rendered)
            except Exception as e:
                print(f"❌ Error rendering chunk: {e}")
        return "\n".join(output)

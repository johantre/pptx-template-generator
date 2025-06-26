from jinja2 import nodes
from jinja2.ext import Extension

class SplitSlideExtension(Extension):
    tags = {"splitslide"}

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        # {% splitslide ticket in "tickets" %}
        target = parser.parse_assign_target()  # e.g. ticket
        parser.stream.expect('name:in')
        collection_expr = parser.parse_expression()  # e.g. "tickets"
        body = parser.parse_statements(['name:endsplitslide'], drop_needle=True)

        # 👇 De CallBlock móét target (e.g. ticket) als kwarg param bevatten:
        return nodes.CallBlock(
            self.call_method('_render_splitslide', args=[
                nodes.Const(target.name),
                collection_expr
            ]),
            [],  # no positional args
            [nodes.Keyword(target.name, nodes.Name(target.name, 'load'))],  # 👈 KEY FIX
            body
        ).set_lineno(lineno)

    def _render_splitslide(self, var_name, collection_name, caller):
        context = self.environment.globals.get("context", {})
        split_config = self.environment.globals.get("split_config", {})

        rows = context.get("collections", {}).get(collection_name, {}).get("rows", [])

        conf = split_config.get(collection_name, {"type": "auto", "max_per_slide": 1})
        max_per_slide = conf.get("max_per_slide", 1)

        if not isinstance(rows, list):
            return caller()

        output = []
        for chunk in [rows[i:i + max_per_slide] for i in range(0, len(rows), max_per_slide)]:
            print(f"DEBUG: rendering chunk with {len(chunk)} items")
            for item in chunk:
                # 🧨 Deze regel veroorzaakt de error als parse() fout is
                output.append(caller(**{var_name: item}))
        return "\n".join(output)

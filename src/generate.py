import os
from jinja2 import Template
import markdown

PAGES_PATH = os.environ.get("PAGES_PATH", "./src/content/pages")
TEMPLATES_PATH = os.environ.get("TEMPLATES_PATH", "./src/content/templates")
SITE_ROOT = os.environ.get("SITE_ROOT", "/out")

engines = {
    # format_extension: (template_string, context) -> html
    "j2": lambda tmpl, ctx: Template(tmpl).render(ctx),
    "md": lambda content, ctx: markdown.markdown(content, **ctx),
    "html": lambda content, _: content,
}

templates = {
    # name: context -> html
}


def load_templates():
    """
    Load all the templates

    The name and format are in the filename
    /templates/root.j2 is a jinja2 template named "root"

    The dictionary should be template names to render functions
    "name": (context -> html)

    """

    print("Loading templates from {}".format(TEMPLATES_PATH))
    formats = {}
    paths = {}
    for root, dirs, files in os.walk(TEMPLATES_PATH):
        for file_name in files:
            name, fmt = file_name.split(".")
            formats[name] = fmt
            path = os.path.join(root, file_name)
            paths[name] = path

    for name, fmt in formats.items():
        with open(paths[name], 'r') as tmpl_file:
            tmpl = tmpl_file.read()
        templates[name] = lambda ctx: engines[fmt](tmpl, ctx)


pages = {
    # path: html string
}

def load_pages():
    """
    Load all the pages

    The name and format are the filename
    pages/index.md is a markdown file with the index content

    Eventually there may be a metadata system to specify what template a page
    should be rendered with, but not yet. It's early

    Everything is then rendered with the root template

    The site structure matches the structure of the pages folder

    """

    print("Loading pages from {}".format(PAGES_PATH))
    for root, dirs, files in os.walk(PAGES_PATH):
        for file_name in files:
            name, fmt = file_name.split(".")
            path = os.path.join(root, "{}.html".format(name))[len(PAGES_PATH):]
            print(path)
            with open(os.path.join(root, file_name), 'r') as pagefile:
                content = pagefile.read()
            pages[path] = engines[fmt](content, {})


def main():
    print("Generating site")
    load_templates()
    root_template = templates.get("root", lambda x: x)
    load_pages()
    for path, html in pages.items():
        file_path = os.path.join(SITE_ROOT, path.strip("/"))
        print(file_path)
        with open(file_path, 'w') as pagefile:
            pagefile.write(
                root_template({"content": html, "title": "Jesse B. Miller"}),
            )


if __name__ == "__main__":
    main()

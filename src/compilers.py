# Compilers :: metacontent -> metacontent

import os
from jinja2 import Template
import markdown
from settings import SITE_ROOT


def format_compiler(metacontent):
    print("format_compiler {}".format(metacontent["__name__"]))
    compiler = compilers[metacontent["__format__"]]
    return compiler(metacontent)


def markdown_compiler(metacontent):
    print("markdown {}".format(metacontent["__name__"]))
    compiled_content = markdown.markdown(
        metacontent["__content__"], **metacontent)
    metacontent["__content__"] = compiled_content
    metacontent["__format__"] = "html"
    return metacontent


def jinja2_compiler_factory(compiler_data):
    def compile_metacontent(metacontent):
        print("jinja2 {}".format(metacontent["__name__"]))
        compiled_content = Template(compiler_data).render(**metacontent)
        metacontent["__content__"] = compiled_content
        metacontent["__format__"] = "html"
        return metacontent

    return compile_metacontent


def make_compiler(compiler_def):
    print("making compiler {}".format(compiler_def))
    builtin_compiler = compilers.get(compiler_def, None)
    if builtin_compiler:
        return builtin_compiler

    # Compiler type is the file extension for the compiler def
    factory_type = compiler_def.split(".")[-1]
    compiler_def_path = os.path.join(SITE_ROOT, compiler_def)
    with open(compiler_def_path, 'r') as compilerfile:
        compiler_data = compilerfile.read()

    def compiler(metacontent):
        return compiler_factories[factory_type](compiler_data)(metacontent)

    return compiler


compilers = {
    "__format__": format_compiler,
    "md": markdown_compiler,
    "markdown": markdown_compiler,
    "html": lambda x: x,
}


compiler_factories = {
    "j2": jinja2_compiler_factory,
    "jinja2": jinja2_compiler_factory,
}

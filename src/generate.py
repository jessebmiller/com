import frontmatter, os, toml, functools
from compilers import make_compiler
from settings import (
    SITE_ROOT,
    SITE_CONFIG,
    TARGET_ROOT,
)


parsers = {
    "toml": lambda data: toml.loads(data)
}


def parse(path):
    """ Parse the contents of the file at path with the appropriate parser """
    fmt = path.split(".")[-1]
    with open(path, 'r') as parsefile:
        return parsers[fmt](parsefile.read())


def get_metacontent(root_meta, path):
    name, fmt = os.path.basename(path).split(".")
    file_metacontent = frontmatter.load(path)
    metacontent = {}
    metacontent.update(root_meta)
    metacontent.update({
        "__content__": file_metacontent.content,
        "__format__": fmt,
        "__name__": name,
        "__dir__": os.path.dirname(path)
    })
    metacontent.update(file_metacontent.metadata)
    return metacontent


def get_meta(root):
    """ find a file named __meta__.* and return it's parsed contents """
    (_, _, filenames) = os.walk(root).__next__()
    for filename in filenames:
        name, fmt = filename.split(".")
        if name == "__meta__":
            with open(os.path.join(root, filename), 'r') as f:
                return parsers[fmt](f.read())

    # No meta file found return empty metadata
    return {}


def compose(*functions):
    return functools.reduce(
        lambda f, g: lambda x: f(g(x)),
        functions,
        lambda x: x,
    )


def compile_metacontent(metacontent):
    # Make a compiler from every compiler listed
    compilers = map(make_compiler, metacontent["__compilers__"])
    # Compose the compilers and run the metacontent through it and return it
    print("\n\nCompiling {}".format(metacontent["__name__"]))
    return compose(*compilers)(metacontent)


def generate(content_dir):
    """
    Given a path to some content, generate it

    """

    # Get all the metacontent
    metacontent = []
    for root, dirs, files in os.walk(content_dir):
        # Each dir may have a directory meta
        meta = get_meta(root)
        meta["__compilers__"].reverse()
        for filename in files:
            # Skip files in dunders and hidden files
            if filename.startswith("."):
                continue
            name, _ = filename.split(".")
            if name.startswith("__") and name.endswith("__"):
                continue
            filepath = os.path.join(root, filename)
            # Each file metacontent is a combination of the folder meta and the
            # file's meta
            metacontent.append(get_metacontent(meta, filepath))

    compiled_content = [compile_metacontent(mc) for mc in metacontent]

    for cc in compiled_content:
        filename = "{}.{}".format(cc["__name__"], cc["__format__"])
        out_path = os.path.join(TARGET_ROOT, filename)
        with open(out_path, 'w') as outfile:
            outfile.write(cc["__content__"])


def main():
    config = parse(SITE_CONFIG)
    for content_dir in config["generate"]:
        run_dir = os.path.dirname(__file__)
        generate(os.path.join(run_dir, content_dir))


if __name__ == "__main__":
    main()

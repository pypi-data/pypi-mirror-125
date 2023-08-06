import click
from joshk.funcs import txt_to_json, to_properties, make_request


@click.command()
@click.option("--bibtex", help="The bibtex to add to notion")
def bibtex_to_notion(bibtex):
    """A method for inserting bibtex entries into notion."""
    bibtex_json = txt_to_json(bibtex)
    properties = to_properties(bibtex_json)
    make_request(properties)


if __name__ == "__main__":
    bibtex_to_notion()

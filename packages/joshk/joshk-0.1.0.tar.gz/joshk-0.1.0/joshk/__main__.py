import click
from bibtex_to_notion.funcs import txt_to_json, to_properties, make_request

@click.command()
@click.option("--bibtex", help="The person to greet.")
def notion_bibtext(bibtex):
    """Simple program that greets NAME for a total of COUNT times."""
    bibtex_json = txt_to_json(bibtex)
    properties = to_properties(bibtex_json)
    make_request(properties)


if __name__ == '__main__':
    notion_bibtext()
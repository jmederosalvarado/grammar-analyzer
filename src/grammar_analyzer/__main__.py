import click
from grammar_analyzer import stapp
from streamlit import cli as stcli


@click.group()
def main():
    pass


@main.command("streamlit")
def main_streamlit():
    filename = stapp.__file__

    if filename.endswith(".pyc"):
        filename = "%s.py" % filename[:-4]

    stcli._main_run(filename, [])


if __name__ == "__main__":
    main()

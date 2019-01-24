#!/usr/bin/env python3

import click
import os.path
import yaml


_NOOTS_LOC = os.path.join(os.path.expanduser('~'), 'noots.yaml')


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('-p', '--pager', is_flag=True)
def cli(ctx, pager):
    if ctx.invoked_subcommand is None:
        if pager:
            show_notes(pager=True)
        else:
            show_notes()


def show_notes(pager=False):
    """
    Display the users saved notes, if any.
    """
    data = _yaml_r() or {}
    categories = sorted([category for category in data])

    output = []

    if data:
        for category in categories:
            output.append(click.style(category, reverse=True))
            for index, item in enumerate(data[category], start=1):
                output.append(' '*3 + str(index) + ': ' + item)
        else:
            if pager:
                click.echo_via_pager('\n'.join(output))
            else:
                for line in output:
                    click.echo(line)
    else:
        click.echo("You don't have any saved notes!")


@cli.command()
@click.argument('note', type=str)
@click.option('-c', '--category')
def r(note, category=None):
    """
    Save a note to noots.

    category is optional and defaults to "General"

    >>> noots remember -c Work "Codereview at 14:00"
    Saves the note to category Work

    >>> noots remember "While out, get eggs."
    Saves the note to the General category
    """
    data = _yaml_r() or {}

    if category is None:
        category = 'General'

    try:
        if note not in data[category]:
            data[category].append(note)
        else:
            click.echo("You've already made this note :)")
    except KeyError:
        data[category] = [note]

    _yaml_w(data)


@cli.command()
@click.argument('category', type=str)
@click.argument('index', type=int)
def f(category, index):
    """
    Deletes notes from noots.
    Removes empty categories.

    >>> noots forget General 2
    Forgets the note marked 2 in the General category
    """
    data = _yaml_r()
    try:
        del data[category][index-1]
    except (KeyError, IndexError, TypeError):
        click.echo('There is no note {} {}'.format(category, index))
        return
    else:
        if data[category] == []:
            del data[category]
    _yaml_w(data)


@cli.command()
@click.argument('category', type=str)
@click.argument('index', type=int)
@click.argument('note', type=str)
def e(category, index, note):
    """
    Replace a note.

    >>> noots edit General 2 "New note"
    Edits replaces the note at General 2 with "New note"
    """
    data = _yaml_r()
    try:
        data[category][index-1] = note
    except KeyError:
        click.echo('There is no note {} {}'.format(category,
                                              index))
        return
    _yaml_w(data)


@cli.command()
def clear():
    """
    Deletes all notes from noots!
    """
    click.echo("These are your notes:")
    show_notes()
    answer = input("Are you sure?(Y/N) > ")
    if answer.casefold().startswith('y'):
        _yaml_w({})
        click.echo("All of your notes have been deleted!")
    else:
        click.echo("Stuff not deleted.")
        return


@cli.command()
def noots():
    click.secho('\n   (o< noot noot!', bold=True)
    click.secho('   //\\', bold=True)
    click.secho('   V_/_\n', bold=True)


def _yaml_r():
    try:
        with open(_NOOTS_LOC, 'r') as noots_file:
            return yaml.load(noots_file)
    except FileNotFoundError:
        with open(_NOOTS_LOC, 'w+'):
            ...
        _yaml_r()


def _yaml_w(data):
    with open(_NOOTS_LOC, 'w') as noots_file:
        yaml.dump(data, noots_file, indent=4, default_flow_style=False)


cli.add_command(r)
cli.add_command(f)
cli.add_command(e)
cli.add_command(clear)

if __name__ == '__main__':
    cli()

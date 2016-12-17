#!/usr/bin/env python3

import argparse
import os.path
import yaml

NOOTS_LOC = os.path.join(os.path.expanduser('~'), 'noots.yaml')


def show_notes():
    """
    Display the users saved notes, if any.

    """
    data = _yaml_r() or {}
    categories = sorted([category for category in data])
    if data:
        for category in categories:
            print('\x1b[3;47;40m' + category + ':' + '\x1b[0m')
            for index, item in enumerate(data[category], start=1):
                print(' '*3, str(index) + ':', item)
    else:
        print("You don't have any saved notes!")


def remember(category, note):
    """
    Save notes to noots

    category is optional and defaults to "General"

    >>> noots remember -c Work "Codereview at 14:00"
    Saves the note to category Work

    >>> noots remember "While out, get eggs."
    Saves the note to the General category
    """
    data = _yaml_r() or {}
    try:
        data[category].append(note[0])
    except KeyError:
        data[category] = [note[0]]
    _yaml_w(data)


def forget(category, index):
    """
    Deletes notes from noots
    Removes empty categories

    Specific category and index required.

    >>> noots forget General 2
    Forgets the note marked 2 in the General category
    """
    data = _yaml_r()
    try:
        del data[category][index-1]
    except (KeyError, IndexError, TypeError):
        print('There is no note {} {}'.format(category,
                                              index))
        return
    else:
        cleanup = []
        for heading in data:
            if data[heading] == []:
                cleanup.append(heading)
        for item in cleanup:
            del data[heading]
    _yaml_w(data)


def edit(category, index, note):
    """
    Allows replacment of note content
    All args required

    >>> noots edit General 2 "New note"
    Edits replaces the note at General 2 with "New note"
    """
    data = _yaml_r()
    try:
        data[category][index-1] = note[0]
    except KeyError:
        print('There is no note {} {}'.format(category,
                                              index))
        return
    _yaml_w(data)


def clear_all():
    """
    Deletes all notes from noots!

             (o<= noot noot!
             //\
             V_/_

    """
    print("These are your notes:")
    show_notes()
    answer = input("Are you sure?(Y/N) > ")
    if answer.lower().startswith('y'):
        _yaml_w({})
        print("All of your notes have been deleted!")
    else:
        print("Stuff not deleted.")
        return


def _yaml_r():
    try:
        with open(NOOTS_LOC, 'r') as noots_file:
            return yaml.load(noots_file)
    except FileNotFoundError:
        temp = open(NOOTS_LOC, 'w+')
        temp.close()
        _yaml_r()


def _yaml_w(data):
    with open(NOOTS_LOC, 'w') as noots_file:
        yaml.dump(data, noots_file, indent=4, default_flow_style=False)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
    description="""
    noots is a cli note taking thing for those who want 
    to view, add, remove and modify their notes quickly and from 
    any directory in their system through their terminal.
    
    Read the docs at
    """
                                     )

    subparsers = parser.add_subparsers(dest="sub_name")

    show_parser = subparsers.add_parser('show')
    show_parser.set_defaults(func='show')

    remember_parser = subparsers.add_parser('r', help='remember')
    remember_parser.add_argument('-c', '--category', default='General')
    remember_parser.add_argument('note', nargs=argparse.ONE_OR_MORE)
    remember_parser.set_defaults(func='remember')

    forget_parser = subparsers.add_parser('f', help='forget')
    forget_parser.add_argument('category')
    forget_parser.add_argument('index', type=int)
    forget_parser.set_defaults(func='forget')

    edit_parser = subparsers.add_parser('e', help='edit')
    edit_parser.add_argument('category', default='General')
    edit_parser.add_argument('index', type=int)
    edit_parser.add_argument('note', nargs=argparse.ONE_OR_MORE)
    edit_parser.set_defaults(func='edit')

    clear_parser = subparsers.add_parser('clear')
    clear_parser.set_defaults(func='clear')

    args = parser.parse_args()

    if args.sub_name is None:
        show_notes()
    elif args.func == 'remember':
        remember(args.category, args.note)

    elif args.func == 'forget':
        forget(args.category, args.index)

    elif args.func == 'edit':
        edit(args.category, args.index, args.note)

    elif args.func == 'clear':
        clear_all()

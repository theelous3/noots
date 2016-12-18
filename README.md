# noots
A command line note taking tool.

## What is noots?

A command line note tool that doesn't involve terminal based editors, and does involve python and YAML.

## Why?

I'm one to try and reduce clutter both on my system and in my head. Keeping track of a small list of things to remember or stuff that needs doing is a pain. Remembering its location, manually accessing it, formatting it and all of the clicking that entails, is something I find unpleasant.

Other command line note tools I've come across are...clunky. They require interacting with vim or nano, and manual formatting. No thank you.

noots takes command line arguments and builds tidy todo/remember lists using the inherent neatness of YAML and a little python splrinkling of magic. The result is a notes system that is easily manipulated both in the command line using noots' interface, or manually in the YAML file.

## What's it look like?

noots has four commands.
* [r]emember
 * [-c] creates or appends to a category
* [f]orget
* [e]dit
* clear

Here's a fancy asciicast of noots in action:
[![asciicast](https://asciinema.org/a/01pj80wc17vt126ue7awy2qek.png)](https://asciinema.org/a/01pj80wc17vt126ue7awy2qek)

## Installation
1. Grab noots.py
2. Place it somewhere that's in your bash's $PATH. Either /bin, /usr/bin or ~/bin
3. Add this line to your .bashrc alias section (which is probably in ~/) -> alias noots='noots.py'

noots requires python3.x and PyYAML.

That should do it. If there are issues, just chmod +x noots.py and it'll probably do the trick.

## Usage

### Showing notes.
Typing `noots` will display your notes.

### Saving notes
Use [r] for remember. Using [r] on its own will save to the default General category, like so:

`$ noots r "my first note"`

Use the -c flag to create a new category or direct a note to an existing category, like this:

`$ noots r -c Shopping "while out, get eggs"`

### Removing notes
Use [f] for forget. [f] requires a category and note number.

To delete the note we made in the Shopping category (and also the category, because it will be empty) we can do:

`$ noots f Shopping 1`

### Editing notes
Use [e] for edit. This is more of a replacement then an edit.

To replace our first note, we can do

`$ noots e General 1 'my first note, edited'`

### Clearing all notes

`$ noots clear`

You will be prompted with a Y/N and given a chance to review your notes before they are deleted.

## Licence

Do whatever you want with noots.

Shoutout to Akuli for guidance through the disaster that is argparse. What a terrible module.

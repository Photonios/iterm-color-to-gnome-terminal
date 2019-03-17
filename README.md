# iterm-color-to-gnome-terminal

Converts iTerm2's *.itemcolors to a gnome-terminal profile.

## Prerequisites
* Python 3.7 or newer

These scripts do not depend on any third-party libraries.

## Usage

    $ ./iterm-colors-to-gnome-terminal.py [*.itemcolors file]

This dumps a new gnome-terminal profile to `stdout`. This profile can be loaded into gnome-terminal using the provided bash script:

    $ ./import-gnome-terminal-profile.py < [file name here]

A complete example of converting a iTerm2 theme and importing it into gnome-terminal:

    $ ./iterm-colors-to-gnome-terminal.py ./mytheme.itermcolors > mytheme.gtp
    $ ./import-gnome-terminal-profile.py < mytheme.gtp

For convenience, both commands can be piped allowing you to the conversion and import in one command:

    $ ./iterm-colors-to-gnome-terminal.py ./mytheme.itermcolors | ./import-gnome-terminal-profile.py

### Profile name
By default, the name of the resulting gnome-terminal profile will be the name of the original iTerm2 file, without the extension. The resulting profile name can be overriden using the `--profile-name` or `-n` flag:

    $ ./import-gnome-terminal-profile.py ./mytheme.itermcolors --profile-name "MyColors"

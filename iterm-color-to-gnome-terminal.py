#!/usr/bin/env python3.7

import sys
import json
import plistlib


def _to_hex(value):
    return "%02X" % int(value * 255)


def _rgb_to_hex(values):
    r = _to_hex(values["Red Component"])
    g = _to_hex(values["Green Component"])
    b = _to_hex(values["Blue Component"])

    return f"#{r}{g}{b}"


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("usage: iterm-color-to-gnome-terminal.py [*.itermcolors file]\n")
        return 1

    file_name = sys.argv[1]
    with open(file_name, "rb") as fp:
        file_contents = fp.read()

    gconf_keys = dict()
    gconf_keys["palette"] = [None] * 16

    colors = plistlib.loads(file_contents)
    for color_name, color_values in colors.items():
        color_value_hex = _rgb_to_hex(color_values)

        if color_name.startswith("Ansi"):
            color_index = int(color_name.replace("Ansi ", "").replace(" Color", ""))
            gconf_keys["palette"][color_index] = color_value_hex

        elif color_name == "Background Color":
            gconf_keys["background_color"] = color_value_hex

        elif color_name == "Foreground Color":
            gconf_keys["foreground_color"] = color_value_hex

        elif color_name == "Bold Color":
            gconf_keys["bold_color"] = color_value_hex

    for index, value in enumerate(gconf_keys["palette"]):
        if not value:
            sys.stderr.write("warning: missing ANSI color {index}\n")

    gconf_keys["palette"] = ",".join(gconf_keys["palette"])

    for key, value in gconf_keys.items():
        print(f"{key} {value}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

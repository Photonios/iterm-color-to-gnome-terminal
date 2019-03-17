#!/usr/bin/env python3.7

import os
import sys
import uuid
import json
import argparse
import plistlib


def _to_hex(value):
    return "%02X" % int(value * 255)


def _rgb_to_hex(values):
    r = _to_hex(values["Red Component"])
    g = _to_hex(values["Green Component"])
    b = _to_hex(values["Blue Component"])

    return f"#{r}{g}{b}"

def _create_gnome_terminal_profile(name, gconf_keys):
    profile_id = str(uuid.uuid4())

    profile_contents = f"[:{profile_id}]\n"
    profile_contents += f"visible-name='{name}'\n"

    for key, value in gconf_keys.items():
        if isinstance(value, list):
            encoded_values = ', '.join([f"'{item}'" for item in value])
            profile_contents += f"{key}=[{encoded_values}]\n"
        else:
            profile_contents += f"{key}='{value}'\n"

    return profile_contents

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", help="Name of the *.itermcolors file to convert")
    parser.add_argument("-n", "--profile-name", type=str, help="Name to give to the result file name (default is the file name)")

    args = parser.parse_args()

    with open(args.file_name, "rb") as fp:
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

    profile_name = args.profile_name or os.path.splitext(args.file_name)[0]
    profile = _create_gnome_terminal_profile(profile_name, gconf_keys)

    print(profile)

    return 0


if __name__ == "__main__":
    sys.exit(main())

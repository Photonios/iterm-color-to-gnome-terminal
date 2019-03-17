#!/usr/bin/env python3.7

import sys
import subprocess


def main():
    profile_contents = list(filter(None, sys.stdin.read().split('\n')))
    profile_id = profile_contents[0][1:-1]

    dconf_path = f"/org/gnome/terminal/legacy/profiles/{profile_id}/"

    dconf = subprocess.Popen(
        [
            "dconf",
            "load",
            dconf_path,
        ],
        stdin=subprocess.PIPE,
    )

    dconf.communicate(input="\n".join(profile_contents).encode("utf-8"))
    return 0


if __name__ == '__main__':
    sys.exit(main())

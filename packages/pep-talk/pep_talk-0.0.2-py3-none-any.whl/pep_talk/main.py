import argparse

from pep_talk.pep_parts import PARTS
from colored import stylize
import colored
import random


def print_pep():
    args = setup_args()

    message: str = ''
    mark_up: str = ''

    for values in PARTS:
        message += values[random.randint(0, len(values) - 1)]

    if args.fg:
        mark_up += colored.fg(args.fg)
    if args.bg:
        mark_up += colored.bg(args.bg)
    if args.attr:
        mark_up += colored.attr(args.attr)

    if mark_up:
        print(stylize(f'{message}', mark_up))
    else:
        print(message)


def setup_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Output some pep! Colors are '
                    'defined here: https://pypi.org/project/colored/')

    parser.add_argument('--fg', help='foreground colour')
    parser.add_argument('--attr', help='text attributes colour, bold etd')
    parser.add_argument('--bg', help='background colour')
    return parser.parse_args()


if __name__ == '__main__':
    print_pep()

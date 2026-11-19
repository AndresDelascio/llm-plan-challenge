"""Resolve the reviewer choice without making a model call."""

import argparse


def route(critic, stakes=None):
    if critic != "auto":
        return critic
    if stakes is None:
        raise ValueError("classify the stakes before using automatic routing")
    return "confirm" if stakes == "consequential" else "codex"


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("critic", choices=("auto", "codex", "claude", "both", "measure"))
    cli.add_argument("--stakes", choices=("routine", "consequential"))
    args = cli.parse_args()
    try:
        print(route(args.critic, args.stakes))
    except ValueError as error:
        cli.error(str(error))


if __name__ == "__main__":
    main()

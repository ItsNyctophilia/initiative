import argparse

import src.initiative_cmd as initiative_cmd
import src.roster as roster


def parse_arguments():
    """Parses the program's command-line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        required=False,
        default=None,
        help="json-formatted file to import",
    )
    return parser.parse_args()


def main():
    """Main Initiative program loop"""
    # Parse arguments
    args = parse_arguments()

    # Set up program loop
    program = initiative_cmd.ProgramLoop()
    program.register_initiative(roster.Initiative())

    # Run import file first if applicable
    if args.file is not None:
        program.do_import(args.file)

    # Execute program loop
    program.cmdloop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Goodbye")
    except Exception as e:
        raise e

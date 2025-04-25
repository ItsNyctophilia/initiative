"""Implements the cmd side of the initiative.py program"""
import cmd


class ProgramLoop(cmd.Cmd):

    """Simple program loop for Initiative.py"""

    prompt = ">"
    intro = """
  ___       _ _   _       _   _           
 |_ _|_ __ (_) |_(_) __ _| |_(_)_   _____ 
  | || '_ \| | __| |/ _` | __| \ \ / / _ \\
  | || | | | | |_| | (_| | |_| |\ V /  __/
 |___|_| |_|_|\__|_|\__,_|\__|_| \_/ \___|
 =========================================\n"""

    def register_initiative(self, initiative_obj):
        """Registers an initiative object to the ProgramLoop"""
        self.initiative = initiative_obj

    def __print_initiative_prelude(self):
        print("Initiative order")
        print("________________")

    def do_print(self, arg):
        """
        Prints the roster without hidden entries or attributes shown

        Usage: print

        This command is intended to provide a printout that can be copied
        and given to players, containing only the necessary information
        required to track initiative order from their end: including
        initiative roll values and the names of entries in the order.

        For a more complete printout that contains information about creature
        HP/AC and/or creatures that are hidden from the initiative order, see
        `hprint`.
        """
        self.__print_initiative_prelude()
        self.initiative.print_roster()

    def do_hprint(self, arg):
        """
        Prints the roster with hidden entries or attributes shown

        Usage: hprint

        This command is intended to provide the DM with all of the
        easily-trackable stat information related to creatures in the initiative
        order, such as Max HP, Current HP, and AC as well as all of the
        information presented by `print`. This also will print any creatures
        that are intended to be hidden from the initiative order, such as
        creatures that are hiding and have not been discovered yet.
        """
        self.__print_initiative_prelude()
        self.initiative.hprint_roster()

    def do_export(self, arg):
        """
        Exports the roster to the given filepath, overwriting the given file

        Usage: export FILEPATH

        This command serializes all of the information about currently-tracked
        entries in the roster and outputs them to the given filepath.

        WARNING: This will overwrite the given file without prompting the user
        for confirmation.
        """
        try:
            self.initiative.export_file(arg)
        # TODO: Improve this
        except (FileNotFoundError, PermissionError) as e:
            raise e

    def do_import(self, arg):
        """
        Import a roster from the given file, overwriting the current roster

        Usage: import FILEPATH

        This command deserializes all of the information from the given file
        and loads it into the current roster.

        WARNING: This will overwrite the current roster with the information
        from the given file. Additionally, passing it an improperly-formatted
        file will cause the program to crash.
        """
        try:
            self.initiative.import_file(arg)
        # TODO: Specifically improve error checking on the file contents
        # and the error messages. Just lazy tbh.
        except (FileNotFoundError, PermissionError) as e:
            print(e)

    def do_toggle_hidden(self, arg):
        """
        Toggle the hidden status on an entry

        Usage: toggle_hidden

        This command toggles whether or not a creature is currently being
        hidden from the initiative order. It does not accept arguments, but
        instead receives its input interactively after passing the command.
        """
        self.do_hprint(None)
        try:
            index = int(input(f"Index of the entry you want to un/hide: "))

            self.initiative.toggle_hidden(index - 1)

        except ValueError:
            print(f"toggle_hidden failed: [FIXME]")

    def do_rename(self, arg):
        """
        Rename an entry

        Usage: rename

        This command will rename the entry at the specified index. It does not
        accept arguments, but instead receives its input interactively after
        passing the command.
        """
        self.do_hprint(None)
        try:
            index = int(input(f"Index of the entry you want to rename: "))
            new_name = input("New name: ")

            self.initiative.rename_entry(index - 1, new_name)

        except ValueError:
            print(f"rename failed: [FIXME]")

    def do_copy(self, arg):
        """
        Copy an entry a number of times

        Usage: copy

        This command will copy the entry a specified number of times. It does
        not accept arguments, but instead receives its input interactively after
        passing the command.

        Note: If the entry's Initiative value was passed manually as opposed
        to having it rolled automagically, then the copies will have the same
        initiative value. Conversely, if they were rolled, the copies will all
        have their initiatives randomly rolled as well.
        """
        self.do_hprint(None)
        try:
            index = int(input(f"Index of the entry you want to copy: "))
            amount = int(input("Number of copies: "))

            self.initiative.copy_index(index - 1, amount)

        except ValueError:
            print(f"copy failed: [FIXME]")

    def __apply_hp_change(self, action_name: str, action_func: callable):
        """Apply a healing or damage action to selected entries by index"""
        self.do_hprint(None)
        # TODO: smarter exception handling
        try:
            response = input(
                f"Indexes of the entries you want to {action_name} (space-separated): "
            )
            amount = int(input("Amount: "))
            for index in response.split():
                index = int(index)
                if index > len(self.initiative.roster.keys()):
                    raise ValueError("Invalid index provided")
                action_func(index - 1, amount)
        except ValueError as e:
            print(f"{action_name} failed:", e)

    def do_heal(self, arg):
        """
        Apply healing to a number of entries

        Usage: heal

        This command will add an amount to the given entries' Current HP values.
        It does not accept arguments, but instead receives its input
        interactively after passing the command.
        """
        self.__apply_hp_change("heal", self.initiative.heal)

    def do_damage(self, arg):
        """
        Apply damage to a number of entries

        Usage: damage

        This command will subtract an amount from the given entries' Current HP
        values. It does not accept arguments, but instead receives its input
        interactively after passing the command.
        """
        self.__apply_hp_change("damage", self.initiative.damage)

    def do_modify(self, arg):
        """
        Apply a modification to an entry's attributes

        Usage: modify

        This command will modify an entry's Initiative, AC, Max HP, or Current
        HP values to the specified number. It does not accept arguments, but
        instead receives its input interactively after passing the command."""
        # Provide hprint for context
        self.do_hprint(None)
        try:
            # Prompt for index of entry
            index = int(input("Index of the entry you want to modify: "))
            if index > len(self.initiative.roster.keys()):
                raise ValueError

            # Prompt for index of field to modify
            options = ("Initiative", "AC", "Max HP", "Current HP")
            for idx, option in enumerate(options, start=1):
                print(f"{idx} {option}")
            key = input("Index of the field you want to modify: ")
            if key == "1":
                key = "initiative"
            elif key == "2":
                key = "ac"
            elif key == "3":
                key = "hp_max"
            elif key == "4":
                key = "hp"
            else:
                print(f"{key} is not a valid index")
                raise ValueError

            value = int(input("Enter a new value: "))

        except ValueError:
            print("modify failed: Invalid index or integer provided")
            return

        self.initiative.modify_index(index - 1, key, value)

    def __validate_add_to_initiative_args(
        self, name, initiative, ac, hp_max, hp, hidden
    ):
        """Validates the arguments passed to add_to_initiative"""
        # Validate that integer fields are numbers
        for field in (initiative, ac, hp_max, hp):
            try:
                int(field)
            except ValueError as e:
                # Only error if initiative is invalid or on noninteger in any
                # integer field
                if field == initiative or field != "":
                    print(f"add_to_initiative failed: {field} is not a number")
                    raise e

    def do_add_to_initiative(self, arg):
        """
        Adds an entry to the initiative roster

        Usage: add_to_initiative

        This command will add a new entry to the initiative roster. You are
        required to enter at least an entry's Name and Initiative values, while
        all other fields can be left blank or filled out, optionally.

        The Initiative field accepts three different formats: 'int', '+int',
        and '-int'. Specifying 'int' will set the initiative value to that
        number, while specifying one of the other two will treat that as an
        initiative modifier and randomly roll for its position in the roster.

        Note: Setting a name that ends with numbers, I.e 'creature 1' can
        potentially break the automatic numbering system in place with the
        `copy` command.
        """
        # Receive parameters from command line
        name = input("Name: ")
        initiative = input("Initiative: ")
        ac = input("AC: ")
        hp_max = input("HP Max: ")
        hp = input("HP Current: ")
        hidden = input("Hidden? [y/n]: ")
        # Check for 'y'-like values in hidden field
        if hidden.lower() in ("y", "ye", "yes"):
            hidden = True
        else:
            hidden = False
        # Package them into a dict
        params = {
            "name": name,
            "initiative": initiative,
            "ac": ac,
            "hp_max": hp_max,
            "hp": hp,
            "hidden": hidden,
        }

        try:
            self.__validate_add_to_initiative_args(**params)
        except ValueError as e:
            pass
        else:
            nonblank_params = {key: value for key, value in params.items() if value}
            if not self.initiative.add_to_initiative(**nonblank_params):
                print(
                    "add_to_initiative failed: entry already exists (use modify instead?)"
                )

    def do_EOF(self, arg):
        raise KeyboardInterrupt

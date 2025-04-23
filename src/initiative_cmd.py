import cmd


class ProgramLoop(cmd.Cmd):

    """Simple program loop for Initiative.py"""

    prompt = ">"
    intro = """
  ___       _ _   _       _   _           
 |_ _|_ __ (_) |_(_) __ _| |_(_)_   _____ 
  | || '_ \| | __| |/ _` | __| \ \ / / _ \\
  | || | | | | |_| | (_| | |_| |\ V /  __/
 |___|_| |_|_|\__|_|\__,_|\__|_| \_/ \___|\n"""
    initiative = None

    def register_initiative(self, initiative_obj):
        """Registers an initiative object to the ProgramLoop"""
        self.initiative = initiative_obj

    def __print_initiative_prelude(self):
        print("Initiative order")
        print("________________")

    def do_print(self, arg):
        """
        Prints the roster

        Usage: print
        """
        self.__print_initiative_prelude()
        self.initiative.print_roster(with_hidden=False)

    def do_hprint(self, arg):
        """
        Prints the roster with hidden members

        Usage: hprint
        """
        self.__print_initiative_prelude()
        self.initiative.print_roster(with_hidden=True)

    def do_export(self, arg):
        """
        Exports the current roster to the given filepath; this will overwrite the given file

        Usage: export FILEPATH
        """
        try:
            self.initiative.export_file(arg)
        # TODO: Improve this
        except (FileNotFoundError, PermissionError) as e:
            raise e

    def do_import(self, arg):
        """
        Import a roster from the given file; this will overwrite the current roster

        Usage: import FILEPATH
        """
        try:
            self.initiative.import_file(arg)
        # TODO: -And this
        except (FileNotFoundError, PermissionError) as e:
            print(e)
    
    def do_toggle_hidden(self, arg):
        pass
    
    def do_copy_entry(self, arg):
        pass

    def do_heal(self, arg):
        """
        Decrement each entry's Current HP value by the given amount

        Usage: heal
        """
        self.do_hprint(None)
        try:
            # Prompt for indexes of entries and healing value
            response = input("Indexes of the entries you want to heal (space-separated): ")
            healing = int(input("Enter amount of healing: "))
            for index in response.split():
                index = int(index)
                if index > len(self.initiative.roster.keys()):
                    raise ValueError


                self.initiative.heal(index - 1, healing)

        except ValueError as e:
            print("heal failed: Invalid index or healing value provided")
            return


    def do_damage(self, arg):
        """
        Decrement each entry's Current HP value by the given amount

        Usage: damage
        """
        self.do_hprint(None)
        try:
            # Prompt for indexes of entries and damage value
            response = input("Indexes of the entries you want to damage (space-separated): ")
            damage = int(input("Enter amount of damage: "))
            for index in response.split():
                index = int(index)
                if index > len(self.initiative.roster.keys()):
                    raise ValueError


                self.initiative.damage(index - 1, damage)

        except ValueError as e:
            print("damage failed: Invalid index or damage value provided")
            return

    def do_modify(self, arg):
        """ """
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
            match key:
                case "1":
                    key = "initiative"
                case "2":
                    key = "ac"
                case "3":
                    key = "hp_max"
                case "4":
                    key = "hp"
                case _:
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
        Adds the given entry to the initiative roster interactively

        Usage: add_to_initiative
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
            self.initiative.add_to_initiative(**nonblank_params)
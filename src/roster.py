import json
from termcolor import colored


class Initiative:

    """"""

    def __init__(self):
        """ """
        self.roster = {}

    def rename_entry(self, key, new_key):
        """ """

    def __decrement_value(self, entry, key, amount):
        """Decrement the specified entry's key's value by amount"""
        self.__increment_value(entry, key, -amount)

    def __increment_value(self, entry, key, amount):
        """Increments the specified entry's key's value by amount"""
        try:
            self.roster[entry][key] += amount
        except (KeyError, TypeError) as e:
            raise e

    def __modify_value(self, entry, key, value):
        """ """
        try:
            self.roster[entry][key] = value
        except KeyError as e:
            raise e
    
    def damage(self, index, amount):
        self.decrement_index(index, "hp", amount)
    
    def heal(self, index, amount):
        self.increment_index(index, "hp", amount)

    def decrement_index(self, index, key, amount):
        self.increment_index(index, key, -amount)

    def increment_index(self, index, key, amount):
        sorted_roster = [
            {name: self.roster[name]}
            for name in sorted(
                self.roster,
                key=lambda name: self.roster[name]["initiative"],
                reverse=True,
            )
        ]
        entry = list(sorted_roster[index])[0]
        self.__increment_value(entry, key, amount)

    def modify_index(self, index, key, value):
        sorted_roster = [
            {name: self.roster[name]}
            for name in sorted(
                self.roster,
                key=lambda name: self.roster[name]["initiative"],
                reverse=True,
            )
        ]
        entry = list(sorted_roster[index])[0]
        self.__modify_value(entry, key, value)

    def print_roster(self, with_hidden=True):
        # TODO: return str instead of printing to terminal directly
        # Iterate through a sorted version of the roster
        for idx, name in enumerate(
            sorted(
                self.roster,
                key=lambda name: int(self.roster[name]["initiative"]),
                reverse=True,
            )
        ):
            entries = self.roster[name]

            # Set defaults for variable string fields
            entry_string = f"{idx + 1}. [{entries['initiative']}] {name}"
            hp_string = ""
            ac_string = ""
            # Only print HP/AC values if not None
            if entries["hp_max"] != 0:
                hp_string = f"({entries['hp']}/{entries['hp_max']} HP)"
                # Colorize health output
                percentage_hp = (
                    int(entries["hp"]) / int(entries["hp_max"]) * 100
                )  # TODO: add try/catch here

                if percentage_hp > 100:
                    hp_string = colored(hp_string, "light_blue")
                elif percentage_hp > 80:
                    hp_string = colored(hp_string, "light_green")
                elif percentage_hp > 50:
                    hp_string = colored(hp_string, "light_yellow")
                elif percentage_hp > 0:
                    hp_string = colored(hp_string, "light_red")
                else:
                    hp_string = colored(hp_string, "red", attrs=["blink"])
            if entries["ac"] != 0:
                ac_string = f"(AC: {entries['ac']})"
            # Combine substrings and print
            if with_hidden:
                # Hidden information includes hidden entries in the initiative
                # as well as the HP and AC values of all creatures
                print(f"{entry_string} {hp_string} {ac_string}")
            else:
                if not self.roster[name]["hidden"]:
                    print(f"{entry_string}")

    def hprint_roster(self):
        self.print_roster(False)

    def import_file(self, path):
        """Imports a json-formatted file as initiative data"""
        with open(path, "r") as fo:
            self.roster = json.load(fo)

    def export_file(self, path):
        """Exports the current initiative data to a file"""
        with open(path, "w") as fo:
            json.dump(self.roster, fo)

    def add_to_initiative(
        self,
        name: str,
        initiative: int,
        ac: int = 0,
        hp_max: int = 0,
        hp: int = 0,
        hidden: bool = False,
    ) -> None:
        """Adds the given entry to the initiative roster"""
        # TODO: Check for existing entry
        self.roster.update(
            {
                name: {
                    "initiative": int(initiative),
                    "ac": int(ac),
                    "hp_max": int(hp_max),
                    "hp": int(hp),
                    "hidden": hidden,
                }
            }
        )
import json
from termcolor import colored

from src.helpers import strlen


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

    def __get_hp_ws(self, hp, hp_max):
        max_hp_entry = max(self.roster.values(), key=lambda x: x["hp"] + x["hp_max"])
        max_hp_entry_len = strlen(max_hp_entry["hp"]) + strlen(max_hp_entry["hp_max"])
        return f"{' ' * (max_hp_entry_len - strlen(hp) - strlen(hp_max))}"

    def __get_name_ws(self, name: str) -> str:
        max_name_len = len(max(self.roster.keys(), key=strlen))
        return f"{' ' * (max_name_len - len(name))}"

    def __get_init_ws(self, max_init_entry_name: str, init_val: int) -> str:
        max_init_len = strlen(self.roster[max_init_entry_name]["initiative"])
        cur_init_len = strlen(init_val)
        return f"{' ' * (max_init_len - cur_init_len)}"

    def __get_idx_ws(self, idx: int) -> str:
        return f"{' ' * (strlen(len(self.roster)) - strlen(idx))}"

    def print_roster(self, with_hidden=False):
        """Prints the roster without hidden information shown"""
        # TODO: return str instead of printing to terminal directly
        # Iterate through a sorted version of the roster

        sorted_roster = sorted(
            self.roster,
            key=lambda name: int(self.roster[name]["initiative"]),
            reverse=True,
        )
        for idx, name in enumerate(sorted_roster, start=1):
            # Printing without hidden info displays only indexes for shown entries
            if not with_hidden:
                idx = sum(
                    1 for n in sorted_roster[:idx] if not self.roster[n]["hidden"]
                )
            entry = self.roster[name]
            # Calling helper functions for variable whitespace calculation
            idx_ws = self.__get_idx_ws(idx)
            init_ws = self.__get_init_ws(sorted_roster[0], entry["initiative"])
            name_ws = self.__get_name_ws(name)
            hp_ws = self.__get_hp_ws(entry["hp"], entry["hp_max"])
            # Set defaults for variable string fields
            entry_string = (
                f"{idx_ws}{idx}. {init_ws}[{entry['initiative']}] {name_ws}{name}"
            )
            hp_string = ""
            ac_string = ""
            # Only print HP/AC values if not None
            if entry["hp_max"] != 0:
                hp_string = f"{hp_ws}({entry['hp']}/{entry['hp_max']} HP)"
                # Colorize health output
                percentage_hp = (
                    int(entry["hp"]) / int(entry["hp_max"]) * 100
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
            if entry["ac"] != 0:
                ac_string = f"(AC: {entry['ac']})"
            # Combine substrings and print
            if with_hidden:
                # Hidden information includes hidden entries in the initiative
                # as well as the HP and AC values of all creatures
                print(f"{entry_string} {hp_string} {ac_string}")
            else:
                if not self.roster[name]["hidden"]:
                    print(f"{entry_string}")

    def hprint_roster(self):
        """Prints the roster with hidden information shown"""
        self.print_roster(True)

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

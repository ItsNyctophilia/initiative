import json
from termcolor import colored
from random import randint
from copy import deepcopy

from src.helpers import strlen
from src.entry import Entry


class Initiative:

    """Class that tracks turn order, stats, and conditions"""

    def __init__(self):
        """ """
        self.roster = {}

    def rename_entry(self, index: int, new_key: str) -> None:
        """ """
        self.roster[new_key] = self.roster.pop(self.get_entry_at_index(index).name)
        self.modify_index(index, "name", new_key)

    # TODO: Put in its own class?
    def roll(
        self, die: int = 20, count: int = 1, modifier: int = 0, advantage: bool = False
    ) -> int:
        """Rolls a number of dice according to the given schema"""
        rolls = []
        for _ in range(0, count):
            if advantage:
                roll = max(randint(1, die), randint(1, die))
            else:
                roll = randint(1, die)
            rolls.append(roll)

        return sum(rolls + modifier)

    def get_entry_at_index(self, index):
        return self.__get_sorted_roster()[index]

    def damage(self, index, amount):
        self.get_entry_at_index(index).damage(amount)

    def heal(self, index, amount):
        self.get_entry_at_index(index).heal(amount)

    def __get_sorted_roster(self):
        # TODO: Maintain internally for efficiency
        return sorted(self.roster.values(), key=lambda x: x.initiative, reverse=True)

    def modify_index(self, index, key, value):
        setattr(self.get_entry_at_index(index), key, value)

    def copy_index(self, index, amount):
        entry = self.get_entry_at_index(index).name

        if not entry.split()[-1].isnumeric():
            self.roster[f"{entry} 1"] = self.roster[entry]
            self.roster[f"{entry} 1"].name = f"{entry} 1"
            self.roster.pop(entry)
            entry = f"{entry} 1"

        existing_copies = sum(
            1 for n in self.roster.keys() if n.split()[:-1] == entry.split()[:-1]
        )
        for _ in range(amount):
            new_entry = f"{' '.join(entry.split()[:-1])} {existing_copies + 1}"
            self.roster[new_entry] = deepcopy(self.roster[entry])
            self.roster[new_entry].name = new_entry
            existing_copies += 1

    def __get_hp_ws(self, hp: int, hp_max: int) -> str:
        max_hp_entry = max(self.roster.values(), key=lambda x: x.hp + x.hp_max)
        max_hp_entry_len = strlen(max_hp_entry.hp) + strlen(max_hp_entry.hp_max)
        return f"{' ' * (max_hp_entry_len - strlen(hp) - strlen(hp_max))}"

    def __get_name_ws(self, name: str) -> str:
        max_name_len = len(max(self.roster.keys(), key=strlen))
        return f"{' ' * (max_name_len - len(name))}"

    def __get_init_ws(self, max_init_entry, current_entry: Entry) -> str:
        max_init_len = strlen(max_init_entry.initiative)
        cur_init_len = strlen(current_entry.initiative)
        return f"{' ' * (max_init_len - cur_init_len)}"

    def __get_idx_ws(self, idx: int) -> str:
        return f"{' ' * (strlen(len(self.roster)) - strlen(idx))}"

    def print_roster(self, with_hidden=False):
        """Prints the roster without hidden information shown"""
        # TODO: return str instead of printing to terminal directly
        # Iterate through a sorted version of the roster

        sorted_roster = self.__get_sorted_roster()
        for idx, entry in enumerate(sorted_roster, start=1):
            # Printing without hidden info displays only indexes for shown entries
            if not with_hidden:
                idx = sum(1 for n in sorted_roster[:idx] if not n.hidden)
            # Calling helper functions for variable whitespace calculation
            idx_ws = self.__get_idx_ws(idx)
            init_ws = self.__get_init_ws(sorted_roster[0], entry)
            name_ws = self.__get_name_ws(entry.name)
            hp_ws = self.__get_hp_ws(entry.hp, entry.hp_max)
            # Set defaults for variable string fields
            entry_string = (
                f"{idx_ws}{idx}. {init_ws}[{entry.initiative}] {name_ws}{entry.name}"
            )
            hp_string = ""
            ac_string = ""
            # Only print HP/AC values if not None
            if entry.hp_max != 0:
                hp_string = f"{hp_ws}({entry.hp}/{entry.hp_max} HP)"
                # Colorize health output
                percentage_hp = (
                    int(entry.hp) / int(entry.hp_max) * 100
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
            if entry.ac != 0:
                ac_string = f"(AC: {entry.ac})"
            # Combine substrings and print
            if with_hidden:
                # Hidden information includes hidden entries in the initiative
                # as well as the HP and AC values of all creatures
                print(f"{entry_string} {hp_string} {ac_string}")
            else:
                if not entry.hidden:
                    print(f"{entry_string}")

    def hprint_roster(self):
        """Prints the roster with hidden information shown"""
        self.print_roster(True)

    def import_file(self, path):
        """Imports a json-formatted file as initiative data"""
        with open(path, "r") as fo:
            data = json.load(fo)
            self.roster = {
                name: Entry.from_dict(entry_data) for name, entry_data in data.items()
            }

    def export_file(self, path):
        """Exports the current initiative data to a file"""
        serializable_roster = {
            name: entry.to_dict() for name, entry in self.roster.items()
        }
        with open(path, "w") as fo:
            json.dump(serializable_roster, fo, indent=2)

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

        # TODO: Check for +/- in initiative to roll
        self.roster[name] = Entry(
            name,
            initiative=int(initiative),
            ac=int(ac),
            hp_max=int(hp_max),
            hp=int(hp),
            hidden=int(hidden),
        )

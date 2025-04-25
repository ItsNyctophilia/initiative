"""Implements the Initiative class, which tracks turn order, stats, and conditions"""
import json

from termcolor import colored
from random import randint
from copy import deepcopy

from src.helpers import strlen
from src.entry import Entry


class Initiative:

    """Class that tracks turn order, stats, and conditions"""

    def __init__(self):
        """Initializes an Initiative object"""
        self.roster = {}

    def toggle_hidden(self, index: int) -> None:
        """Toggles the hidden attribute on the given entry"""
        self.get_entry_at_index(index).toggle_hidden()

    def rename_entry(self, index: int, new_key: str) -> None:
        """Renames an entry and its name attribute to new_key"""
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

        return sum(rolls) + modifier

    def get_entry_at_index(self, index: int) -> None:
        """Returns the Entity object at the specified index from the roster"""
        return self.__get_sorted_roster()[index]

    def damage(self, index: int, amount: int) -> None:
        """Damage the entity at index by amount"""
        self.get_entry_at_index(index).damage(amount)

    def heal(self, index: int, amount: int) -> None:
        """Heal the entity at index by amount"""
        self.get_entry_at_index(index).heal(amount)

    def __get_sorted_roster(self):
        """Returns the roster as a list, sorted by initiative value desc."""
        # TODO: Maintain internally for efficiency
        return sorted(self.roster.values(), key=lambda x: x.initiative, reverse=True)

    def modify_index(self, index: int, attribute: int, value: int) -> None:
        """Modifies the entry at index's attribute to the specified value"""
        setattr(self.get_entry_at_index(index), attribute, value)

    def copy_index(self, index: int, amount: int) -> None:
        """Copies the entry at the given index amount number of times"""
        entry = self.get_entry_at_index(index).name

        # If name does not end with a number, rename it to 'name 1'
        if not entry.split()[-1].isnumeric():
            self.rename_entry(index, f"{entry} 1")
            entry = f"{entry} 1"
        # Count the number of entities with the same name
        existing_copies = sum(
            1 for n in self.roster.keys() if n.split()[:-1] == entry.split()[:-1]
        )
        # Create amount number of copies of the specified entry
        for _ in range(amount):
            new_entry = f"{' '.join(entry.split()[:-1])} {existing_copies + 1}"
            self.roster[new_entry] = deepcopy(self.roster[entry])
            self.roster[new_entry].name = new_entry
            # If initiative bonus is not 0, reroll initiative using that bonus
            if self.roster[new_entry].init_bonus:
                self.roster[new_entry].initiative = self.roll(
                    modifier=self.roster[new_entry].init_bonus
                )
            existing_copies += 1

    def __get_hp_ws(self, hp: int, hp_max: int) -> str:
        """Helper function to right justify the whitespace for '(hp)'"""
        max_hp_entry = max(self.roster.values(), key=lambda x: x.hp + x.hp_max)
        max_hp_entry_len = strlen(max_hp_entry.hp) + strlen(max_hp_entry.hp_max)
        return f"{' ' * (max_hp_entry_len - strlen(hp) - strlen(hp_max))}"

    def __get_name_ws(self, name: str) -> str:
        """Helper function to right justify the whitespace for 'name'"""
        max_name_len = len(max(self.roster.keys(), key=strlen))
        return f"{' ' * (max_name_len - len(name))}"

    def __get_init_ws(self, max_init_entry, current_entry: Entry) -> str:
        """Helper function to right justify the whitespace for '[init]'"""
        max_init_len = strlen(max_init_entry.initiative)
        cur_init_len = strlen(current_entry.initiative)
        return f"{' ' * (max_init_len - cur_init_len)}"

    def __get_idx_ws(self, idx: int) -> str:
        """Helper function to right justify the whitespace for 'idx.'"""
        return f"{' ' * (strlen(len(self.roster)) - strlen(idx))}"

    def print_roster(self, with_hidden: bool = False) -> None:
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

    def hprint_roster(self) -> None:
        """Prints the roster with hidden information shown"""
        self.print_roster(True)

    def import_file(self, path: str) -> None:
        """Imports a json-formatted file as initiative data"""
        with open(path, "r") as fo:
            data = json.load(fo)
            self.roster = {
                name: Entry.from_dict(entry_data) for name, entry_data in data.items()
            }

    def export_file(self, path: str) -> None:
        """Exports the current initiative data to a file"""
        serializable_roster = {
            name: entry.to_dict() for name, entry in self.roster.items()
        }
        with open(path, "w") as fo:
            json.dump(serializable_roster, fo, indent=2)

    def add_to_initiative(
        self,
        name: str,
        initiative: str,
        ac: int = 0,
        hp_max: int = 0,
        hp: int = 0,
        hidden: bool = False,
    ) -> bool:
        """Adds the given entry to the initiative roster"""
        # Check if name already exists in roster; return False if so
        if self.roster.get(name, False):
            return False
        # Create roster entry object
        self.roster[name] = Entry(
            name,
            ac=int(ac),
            hp_max=int(hp_max),
            hp=int(hp),
            hidden=int(hidden),
        )
        # '+/-' indicates an initiative bonus and will be rolled automagically
        if initiative.startswith("+") or initiative.startswith("-"):
            self.roster[name].init_bonus = int(initiative)
            self.roster[name].initiative = self.roll(modifier=int(initiative))
        # Otherwise initiative is considered explicit and will be set
        else:
            self.roster[name].initiative = int(initiative)

        return True
